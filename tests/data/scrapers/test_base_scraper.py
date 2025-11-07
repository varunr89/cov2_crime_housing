import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import pandas as pd
from src.data.scrapers.base_scraper import BaseScraper


class ConcreteScraper(BaseScraper):
    """Concrete implementation for testing."""

    def scrape(self) -> pd.DataFrame:
        """Mock scrape implementation."""
        return pd.DataFrame({'col1': [1, 2, 3]})


class TestBaseScraper:
    """Test base scraper functionality."""

    def test_initialization(self, tmp_path):
        """Test scraper initialization."""
        config = {
            'name': 'Test Scraper',
            'output_file': 'test.csv',
            'output_dir': 'raw',
            'rate_limit_seconds': 2,
            'max_retries': 3
        }

        scraper = ConcreteScraper(
            name='test_scraper',
            config=config,
            project_root=str(tmp_path)
        )

        assert scraper.name == 'test_scraper'
        assert scraper.config == config
        assert scraper.rate_limit_seconds == 2
        assert scraper.max_retries == 3

    def test_get_output_path(self, tmp_path):
        """Test output path generation."""
        config = {
            'name': 'Test Scraper',
            'output_file': 'test.csv',
            'output_dir': 'raw'
        }

        # Create data directory
        data_dir = tmp_path / 'data' / '1_raw'
        data_dir.mkdir(parents=True)

        scraper = ConcreteScraper(
            name='test_scraper',
            config=config,
            project_root=str(tmp_path)
        )

        output_path = scraper.get_output_path()
        expected = data_dir / 'test.csv'

        assert output_path == expected

    def test_save_data(self, tmp_path):
        """Test saving DataFrame to CSV."""
        config = {
            'name': 'Test Scraper',
            'output_file': 'test.csv',
            'output_dir': 'raw'
        }

        data_dir = tmp_path / 'data' / '1_raw'
        data_dir.mkdir(parents=True)

        scraper = ConcreteScraper(
            name='test_scraper',
            config=config,
            project_root=str(tmp_path)
        )

        df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        scraper.save_data(df)

        output_file = data_dir / 'test.csv'
        assert output_file.exists()

        loaded_df = pd.read_csv(output_file)
        pd.testing.assert_frame_equal(df, loaded_df)

    def test_run_executes_scrape_and_save(self, tmp_path):
        """Test that run() executes scraping and saves data."""
        config = {
            'name': 'Test Scraper',
            'output_file': 'test.csv',
            'output_dir': 'raw'
        }

        data_dir = tmp_path / 'data' / '1_raw'
        data_dir.mkdir(parents=True)

        scraper = ConcreteScraper(
            name='test_scraper',
            config=config,
            project_root=str(tmp_path)
        )

        result = scraper.run()

        assert result is True
        output_file = data_dir / 'test.csv'
        assert output_file.exists()

    @patch('time.sleep')
    def test_rate_limiting(self, mock_sleep, tmp_path):
        """Test that rate limiting is applied."""
        config = {
            'name': 'Test Scraper',
            'output_file': 'test.csv',
            'output_dir': 'raw',
            'rate_limit_seconds': 2
        }

        scraper = ConcreteScraper(
            name='test_scraper',
            config=config,
            project_root=str(tmp_path)
        )

        scraper.apply_rate_limit()
        mock_sleep.assert_called_once_with(2)
