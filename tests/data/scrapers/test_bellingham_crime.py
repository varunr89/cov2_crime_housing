import pytest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
from datetime import datetime
from src.data.scrapers.bellingham_crime import BellinghamCrimeScraper


class TestBellinghamCrimeScraper:
    """Test Bellingham crime scraper."""

    @pytest.fixture
    def mock_config(self):
        """Provide mock configuration."""
        return {
            'name': 'Bellingham Police Activity',
            'url': 'https://police.cob.org/PIRPressSummary/ReleaseForm.aspx',
            'output_file': 'COB_CrimeReport.csv',
            'output_dir': 'interim',
            'start_year': 2020,
            'end_year': 2021,
            'rate_limit_seconds': 0,
            'max_retries': 3,
            'timeout': 30
        }

    def test_initialization(self, mock_config, tmp_path):
        """Test scraper initialization."""
        scraper = BellinghamCrimeScraper(
            name='bellingham_crime',
            config=mock_config,
            project_root=str(tmp_path)
        )

        assert scraper.name == 'bellingham_crime'
        assert scraper.start_year == 2020
        assert scraper.end_year == 2021
        assert scraper.base_url == 'https://police.cob.org/PIRPressSummary/ReleaseForm.aspx'

    def test_get_form_tokens(self, mock_config, tmp_path):
        """Test extraction of ASP.NET form tokens."""
        scraper = BellinghamCrimeScraper(
            name='bellingham_crime',
            config=mock_config,
            project_root=str(tmp_path)
        )

        # Mock the session.get method
        mock_response = Mock()
        mock_response.text = '''
        <html>
            <input name="__VIEWSTATE" value="test_viewstate" />
            <input name="__VIEWSTATEGENERATOR" value="test_generator" />
            <input name="__EVENTVALIDATION" value="test_validation" />
        </html>
        '''
        mock_response.raise_for_status = Mock()
        scraper.session.get = Mock(return_value=mock_response)

        tokens = scraper._get_form_tokens()

        assert tokens['__VIEWSTATE'] == 'test_viewstate'
        assert tokens['__VIEWSTATEGENERATOR'] == 'test_generator'
        assert tokens['__EVENTVALIDATION'] == 'test_validation'

    def test_scrape_month_data(self, mock_config, tmp_path):
        """Test scraping data for a single month."""
        scraper = BellinghamCrimeScraper(
            name='bellingham_crime',
            config=mock_config,
            project_root=str(tmp_path)
        )

        # Mock GET for tokens
        mock_get_response = Mock()
        mock_get_response.text = '''
        <input name="__VIEWSTATE" value="vs" />
        <input name="__VIEWSTATEGENERATOR" value="vsg" />
        <input name="__EVENTVALIDATION" value="ev" />
        '''
        mock_get_response.raise_for_status = Mock()

        # Mock POST response with crime data
        mock_post_response = Mock()
        mock_post_response.text = '''
        <html>
        <body>
        <table>
            <tr><th>Date</th><th>Location</th><th>Offence</th></tr>
            <tr>
                <td>01/15/2020</td>
                <td>123 Main St</td>
                <td>Theft - Case #2020-001</td>
            </tr>
        </table>
        </body>
        </html>
        '''
        mock_post_response.raise_for_status = Mock()

        # Mock the session methods
        scraper.session.get = Mock(return_value=mock_get_response)
        scraper.session.post = Mock(return_value=mock_post_response)

        df = scraper._scrape_month(2020, 1)

        assert len(df) == 1
        assert 'Date' in df.columns
        assert 'Location' in df.columns
        assert 'Offence' in df.columns

    @patch('src.data.scrapers.bellingham_crime.BellinghamCrimeScraper._scrape_month')
    def test_scrape_full_range(self, mock_scrape_month, mock_config, tmp_path):
        """Test scraping full date range."""
        # Mock _scrape_month to return sample data
        mock_scrape_month.return_value = pd.DataFrame({
            'Date': ['01/15/2020'],
            'Location': ['123 Main St'],
            'Offence': ['Theft'],
            'Crime Category': ['Property'],
            'Case Details': ['#2020-001']
        })

        # Limit to small range for testing
        mock_config['start_year'] = 2020
        mock_config['end_year'] = 2020

        scraper = BellinghamCrimeScraper(
            name='bellingham_crime',
            config=mock_config,
            project_root=str(tmp_path)
        )

        df = scraper.scrape()

        # Should have called _scrape_month 12 times (12 months in 2020)
        assert mock_scrape_month.call_count == 12
        assert len(df) == 12  # 1 record per month
