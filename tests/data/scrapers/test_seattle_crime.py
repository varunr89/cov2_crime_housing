import pytest
from unittest.mock import Mock, patch
import pandas as pd
from src.data.scrapers.seattle_crime import SeattleCrimeScraper


class TestSeattleCrimeScraper:
    """Test Seattle crime scraper."""

    @pytest.fixture
    def mock_config(self):
        """Provide mock configuration."""
        return {
            'name': 'Seattle Police Crime Data',
            'url': 'https://data.seattle.gov/resource/tazs-3rd5.json',
            'output_file': 'Seattle_Crime_Data.csv',
            'output_dir': 'raw',
            'limit': 1000,
            'rate_limit_seconds': 0,
            'max_retries': 3,
            'timeout': 60
        }

    def test_initialization(self, mock_config, tmp_path):
        """Test scraper initialization."""
        scraper = SeattleCrimeScraper(
            name='seattle_crime',
            config=mock_config,
            project_root=str(tmp_path)
        )

        assert scraper.name == 'seattle_crime'
        assert scraper.api_url == 'https://data.seattle.gov/resource/tazs-3rd5.json'
        assert scraper.limit == 1000

    @patch('src.data.scrapers.seattle_crime.requests.get')
    def test_scrape_api_data(self, mock_get, mock_config, tmp_path):
        """Test scraping data from API."""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                'report_number': '2020-001',
                'offense': 'Theft',
                'offense_code': '2399',
                'occurred_date_or_date_range_start': '2020-01-15T10:00:00',
                'latitude': '47.6062',
                'longitude': '-122.3321'
            },
            {
                'report_number': '2020-002',
                'offense': 'Assault',
                'offense_code': '1399',
                'occurred_date_or_date_range_start': '2020-01-16T14:30:00',
                'latitude': '47.6101',
                'longitude': '-122.3420'
            }
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        scraper = SeattleCrimeScraper(
            name='seattle_crime',
            config=mock_config,
            project_root=str(tmp_path)
        )

        df = scraper.scrape()

        assert len(df) == 2
        assert 'report_number' in df.columns
        assert 'offense' in df.columns
        mock_get.assert_called_once()

    @patch('src.data.scrapers.seattle_crime.requests.get')
    def test_scrape_handles_empty_response(self, mock_get, mock_config, tmp_path):
        """Test handling empty API response."""
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        scraper = SeattleCrimeScraper(
            name='seattle_crime',
            config=mock_config,
            project_root=str(tmp_path)
        )

        df = scraper.scrape()

        assert df.empty
