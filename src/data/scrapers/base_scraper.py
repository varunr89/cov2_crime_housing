"""Base scraper class for all web scrapers."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional
import time
import logging
import pandas as pd

from src.data.utils.logger import get_logger


class BaseScraper(ABC):
    """Abstract base class for all scrapers."""

    def __init__(
        self,
        name: str,
        config: Dict[str, Any],
        project_root: Optional[str] = None
    ):
        """
        Initialize base scraper.

        Args:
            name: Scraper identifier
            config: Scraper configuration dictionary
            project_root: Project root directory path
        """
        self.name = name
        self.config = config
        self.project_root = Path(project_root) if project_root else Path.cwd()

        # Extract common configuration
        self.scraper_name = config.get('name', name)
        self.output_file = config.get('output_file')
        self.output_dir = config.get('output_dir', 'raw')
        self.rate_limit_seconds = config.get('rate_limit_seconds', 2)
        self.max_retries = config.get('max_retries', 3)
        self.timeout = config.get('timeout', 30)

        # Set up logging
        self.logger = get_logger(f'scraper.{name}')
        if not self.logger.handlers:
            self.logger = logging.getLogger(f'scraper.{name}')
            self.logger.setLevel(logging.INFO)

    @abstractmethod
    def scrape(self) -> pd.DataFrame:
        """
        Scrape data from source.

        Returns:
            DataFrame containing scraped data
        """
        pass

    def get_output_path(self) -> Path:
        """
        Get full output file path.

        Returns:
            Absolute path to output file
        """
        # Map output_dir to actual directory
        dir_mapping = {
            'external': '0_external',
            'raw': '1_raw',
            'interim': '2_interim',
            'processed': '3_processed'
        }

        actual_dir = dir_mapping.get(self.output_dir, self.output_dir)
        output_dir = self.project_root / 'data' / actual_dir
        output_dir.mkdir(parents=True, exist_ok=True)

        return output_dir / self.output_file

    def save_data(self, df: pd.DataFrame) -> None:
        """
        Save DataFrame to CSV file.

        Args:
            df: DataFrame to save
        """
        output_path = self.get_output_path()
        df.to_csv(output_path, index=False)
        self.logger.info(f"Saved {len(df)} records to {output_path}")

    def run(self) -> bool:
        """
        Execute the complete scraping workflow.

        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info(f"Starting scraper: {self.scraper_name}")

            # Scrape data
            df = self.scrape()

            # Validate data
            if df is None or df.empty:
                self.logger.warning("No data scraped")
                return False

            # Save data
            self.save_data(df)

            self.logger.info(f"Successfully completed scraper: {self.scraper_name}")
            return True

        except Exception as e:
            self.logger.error(f"Error in scraper {self.name}: {e}", exc_info=True)
            return False

    def apply_rate_limit(self) -> None:
        """Apply rate limiting delay."""
        if self.rate_limit_seconds > 0:
            time.sleep(self.rate_limit_seconds)
