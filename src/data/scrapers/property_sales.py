"""Whatcom County property sales scraper using Selenium."""
from typing import Dict
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from tenacity import retry, stop_after_attempt, wait_exponential

from src.data.scrapers.base_scraper import BaseScraper
from src.data.utils.selenium_helper import create_driver, quit_driver


class PropertySalesScraper(BaseScraper):
    """Scraper for Whatcom County property sales."""

    def __init__(self, name: str, config: Dict, project_root: str = None):
        """Initialize property sales scraper."""
        super().__init__(name, config, project_root)

        self.base_url = config['url']
        self.max_pages = config.get('max_pages', 200)
        self.headless = config.get('headless', True)

    def _scrape_page(self, driver, page_num: int) -> pd.DataFrame:
        """
        Scrape a single page of property sales.

        Args:
            driver: Selenium WebDriver instance
            page_num: Page number to scrape

        Returns:
            DataFrame containing property sales from the page
        """
        self.logger.info(f"Scraping page {page_num}")

        # Parse page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        records = []

        # Find sales table
        table = soup.find('table', {'id': 'GridView1'})
        if not table:
            return pd.DataFrame()

        rows = table.find_all('tr')[1:]  # Skip header

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 4:
                # Extract link
                link_tag = cols[0].find('a')
                link = link_tag['href'] if link_tag else ''

                # Extract fields
                address = cols[1].get_text(strip=True)
                sale_date = cols[2].get_text(strip=True)
                sale_price = cols[3].get_text(strip=True)

                records.append({
                    'Assessor Link': link,
                    'Address': address,
                    'Sale Date': sale_date,
                    'Sale Price': sale_price
                })

        return pd.DataFrame(records)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def scrape(self) -> pd.DataFrame:
        """
        Scrape property sales data.

        Returns:
            DataFrame containing all property sales
        """
        driver = None
        all_data = []

        try:
            # Create WebDriver
            driver = create_driver(headless=self.headless)
            driver.get(self.base_url)

            # Wait for page to load
            WebDriverWait(driver, self.timeout).until(
                EC.presence_of_element_located((By.ID, 'GridView1'))
            )

            # Scrape first page
            page_data = self._scrape_page(driver, 1)
            if not page_data.empty:
                all_data.append(page_data)

            # Navigate through pages
            for page_num in range(2, self.max_pages + 1):
                try:
                    # Find and click next page button
                    next_button = driver.find_element(By.LINK_TEXT, str(page_num))
                    next_button.click()

                    # Wait for page to load
                    WebDriverWait(driver, self.timeout).until(
                        EC.presence_of_element_located((By.ID, 'GridView1'))
                    )

                    # Scrape page
                    page_data = self._scrape_page(driver, page_num)
                    if not page_data.empty:
                        all_data.append(page_data)

                    # Apply rate limiting
                    self.apply_rate_limit()

                except (NoSuchElementException, TimeoutException) as e:
                    self.logger.warning(f"Stopped at page {page_num}: {e}")
                    break

            if all_data:
                return pd.concat(all_data, ignore_index=True)
            else:
                return pd.DataFrame()

        finally:
            quit_driver(driver)
