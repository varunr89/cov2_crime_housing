import pytest
from unittest.mock import Mock, patch
import pandas as pd
from src.data.scrapers.property_sales import PropertySalesScraper


class TestPropertySalesScraper:
    """Test property sales scraper."""

    @pytest.fixture
    def mock_config(self):
        """Provide mock configuration."""
        return {
            'name': 'Whatcom County Property Sales',
            'url': 'https://property.whatcomcounty.us/PropertyAccess/SearchResultsSales.aspx',
            'output_file': 'Bellingham_Property_Part1.csv',
            'output_dir': 'interim',
            'max_pages': 2,
            'headless': True,
            'rate_limit_seconds': 0,
            'max_retries': 3,
            'timeout': 30
        }

    def test_initialization(self, mock_config, tmp_path):
        """Test scraper initialization."""
        scraper = PropertySalesScraper(
            name='property_sales',
            config=mock_config,
            project_root=str(tmp_path)
        )

        assert scraper.name == 'property_sales'
        assert scraper.max_pages == 2
        assert scraper.headless is True
