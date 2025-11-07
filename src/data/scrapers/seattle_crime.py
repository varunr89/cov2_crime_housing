"""Seattle Police crime data scraper via Socrata API."""
from typing import Dict
import pandas as pd
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from src.data.scrapers.base_scraper import BaseScraper


class SeattleCrimeScraper(BaseScraper):
    """Scraper for Seattle Police crime data via public API."""

    def __init__(self, name: str, config: Dict, project_root: str = None):
        """Initialize Seattle crime scraper."""
        super().__init__(name, config, project_root)

        self.api_url = config['url']
        self.limit = config.get('limit', 1000000)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def scrape(self) -> pd.DataFrame:
        """
        Scrape crime data from Seattle Open Data API.

        Returns:
            DataFrame containing crime records
        """
        self.logger.info(f"Fetching up to {self.limit} records from Seattle API")

        # Build query parameters
        params = {
            '$limit': self.limit,
            '$order': 'occurred_date_or_date_range_start DESC'
        }

        # Make API request
        response = requests.get(
            self.api_url,
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()

        # Parse JSON response
        data = response.json()

        if not data:
            self.logger.warning("No data returned from API")
            return pd.DataFrame()

        # Convert to DataFrame
        df = pd.json_normalize(data)

        self.logger.info(f"Successfully fetched {len(df)} records")

        return df
