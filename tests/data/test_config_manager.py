import pytest
from pathlib import Path
from src.data.config_manager import ConfigManager


class TestConfigManager:
    """Test configuration management functionality."""

    def test_load_config(self, tmp_path):
        """Test loading configuration from YAML file."""
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text("""
project:
  name: test_project
  version: 1.0.0

data_dirs:
  raw: data/raw
  processed: data/processed

logging:
  level: INFO
  file: logs/test.log
""")

        config = ConfigManager(config_path=str(config_file))
        assert config.get('project.name') == 'test_project'
        assert config.get('project.version') == '1.0.0'
        assert config.get('data_dirs.raw') == 'data/raw'

    def test_get_nested_value(self, tmp_path):
        """Test getting nested configuration values using dot notation."""
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text("""
scrapers:
  bellingham_crime:
    enabled: true
    url: https://example.com
""")

        config = ConfigManager(config_path=str(config_file))
        assert config.get('scrapers.bellingham_crime.enabled') is True
        assert config.get('scrapers.bellingham_crime.url') == 'https://example.com'

    def test_get_with_default(self, tmp_path):
        """Test getting value with default fallback."""
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text("project:\n  name: test")

        config = ConfigManager(config_path=str(config_file))
        assert config.get('nonexistent.key', default='fallback') == 'fallback'

    def test_get_scraper_config(self, tmp_path):
        """Test getting complete scraper configuration."""
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text("""
scrapers:
  test_scraper:
    enabled: true
    url: https://test.com
    output_file: test.csv
""")

        config = ConfigManager(config_path=str(config_file))
        scraper_config = config.get_scraper_config('test_scraper')

        assert scraper_config['enabled'] is True
        assert scraper_config['url'] == 'https://test.com'
        assert scraper_config['output_file'] == 'test.csv'

    def test_get_data_dir(self, tmp_path):
        """Test getting absolute path to data directory."""
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text("""
data_dirs:
  raw: data/1_raw
  interim: data/2_interim
""")

        config = ConfigManager(config_path=str(config_file), project_root=str(tmp_path))
        raw_dir = config.get_data_dir('raw')

        assert raw_dir == tmp_path / 'data' / '1_raw'
        assert isinstance(raw_dir, Path)
