"""Bellingham Police Activity scraper."""
import re
from datetime import datetime
from typing import Dict, List
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

from src.data.scrapers.base_scraper import BaseScraper


class BellinghamCrimeScraper(BaseScraper):
    """Scraper for Bellingham Police Activity reports."""

    def __init__(self, name: str, config: Dict, project_root: str = None):
        """Initialize Bellingham crime scraper."""
        super().__init__(name, config, project_root)

        self.base_url = config['url']
        self.start_year = config.get('start_year', 2015)
        self.end_year = config.get('end_year', datetime.now().year)

        self.session = requests.Session()

    def _get_form_tokens(self) -> Dict[str, str]:
        """
        Extract ASP.NET form tokens from the page.

        Returns:
            Dictionary containing __VIEWSTATE, __VIEWSTATEGENERATOR, __EVENTVALIDATION
        """
        response = self.session.get(self.base_url, timeout=self.timeout)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        tokens = {
            '__VIEWSTATE': soup.find('input', {'name': '__VIEWSTATE'})['value'],
            '__VIEWSTATEGENERATOR': soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value'],
            '__EVENTVALIDATION': soup.find('input', {'name': '__EVENTVALIDATION'})['value']
        }

        return tokens

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _scrape_month(self, year: int, month: int) -> pd.DataFrame:
        """
        Scrape crime data for a specific month.

        Args:
            year: Year to scrape
            month: Month to scrape (1-12)

        Returns:
            DataFrame containing crime records for the month
        """
        self.logger.info(f"Scraping data for {year}-{month:02d}")

        # Get form tokens
        tokens = self._get_form_tokens()

        # Calculate date range (first to last day of month)
        start_date = f"{month}/01/{year}"
        if month == 12:
            end_date = f"12/31/{year}"
        else:
            # Last day of month
            next_month = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
            last_day = (next_month - pd.Timedelta(days=1)).day
            end_date = f"{month}/{last_day}/{year}"

        # Prepare POST data
        form_data = {
            '__VIEWSTATE': tokens['__VIEWSTATE'],
            '__VIEWSTATEGENERATOR': tokens['__VIEWSTATEGENERATOR'],
            '__EVENTVALIDATION': tokens['__EVENTVALIDATION'],
            'ctl00$ContentPlaceHolder1$txtStartDate': start_date,
            'ctl00$ContentPlaceHolder1$txtEndDate': end_date,
            'ctl00$ContentPlaceHolder1$btnSubmit': 'Submit'
        }

        # Submit form
        response = self.session.post(self.base_url, data=form_data, timeout=self.timeout)
        response.raise_for_status()

        # Parse results
        soup = BeautifulSoup(response.text, 'html.parser')
        records = []

        # Find table rows
        table = soup.find('table')
        if table:
            rows = table.find_all('tr')[1:]  # Skip header row

            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    # Extract data
                    date_str = cols[0].get_text(strip=True)
                    location = cols[1].get_text(strip=True)
                    offence_full = cols[2].get_text(strip=True)

                    # Parse offence and case details
                    match = re.match(r'(.*?)\s*-\s*Case\s*#?\s*(.+)', offence_full)
                    if match:
                        offence = match.group(1).strip()
                        case_details = match.group(2).strip()
                    else:
                        offence = offence_full
                        case_details = ''

                    # Categorize crime (simple categorization)
                    crime_category = self._categorize_crime(offence)

                    records.append({
                        'Date': date_str,
                        'Location': location,
                        'Offence': offence,
                        'Crime Category': crime_category,
                        'Case Details': case_details
                    })

        # Apply rate limiting
        self.apply_rate_limit()

        return pd.DataFrame(records)

    def _categorize_crime(self, offence: str) -> str:
        """
        Categorize crime based on offence description.

        Args:
            offence: Offence description

        Returns:
            Crime category
        """
        offence_lower = offence.lower()

        if any(word in offence_lower for word in ['theft', 'burglary', 'robbery', 'stolen']):
            return 'Property'
        elif any(word in offence_lower for word in ['assault', 'battery', 'homicide', 'violence']):
            return 'Violent'
        elif any(word in offence_lower for word in ['drug', 'narcotic', 'controlled substance']):
            return 'Drug'
        elif any(word in offence_lower for word in ['traffic', 'dui', 'driving']):
            return 'Traffic'
        else:
            return 'Other'

    def scrape(self) -> pd.DataFrame:
        """
        Scrape all crime data for configured date range.

        Returns:
            DataFrame containing all crime records
        """
        all_data = []

        for year in range(self.start_year, self.end_year + 1):
            for month in range(1, 13):
                try:
                    month_data = self._scrape_month(year, month)
                    if not month_data.empty:
                        all_data.append(month_data)
                except Exception as e:
                    self.logger.error(f"Error scraping {year}-{month:02d}: {e}")
                    continue

        if all_data:
            return pd.concat(all_data, ignore_index=True)
        else:
            return pd.DataFrame()
