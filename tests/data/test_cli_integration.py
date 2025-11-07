import pytest
from click.testing import CliRunner
from unittest.mock import Mock, patch, MagicMock
from src.data.cli import cli, update, status
import pandas as pd


class TestCLIIntegration:
    """Integration tests for CLI commands."""

    def test_cli_help(self):
        """Test main CLI help."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])

        assert result.exit_code == 0
        assert 'Unified web scraper CLI' in result.output
        assert 'update' in result.output
        assert 'status' in result.output

    def test_cli_version(self):
        """Test CLI version."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--version'])

        assert result.exit_code == 0
        assert '0.2.0' in result.output

    def test_update_help(self):
        """Test update command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ['update', '--help'])

        assert result.exit_code == 0
        assert 'Update data from web sources' in result.output
        assert '--all' in result.output
        assert '--bellingham-crime' in result.output

    def test_update_no_scrapers_selected(self):
        """Test update with no scrapers shows error."""
        runner = CliRunner()
        result = runner.invoke(cli, ['update'])

        assert result.exit_code == 0
        assert 'No scrapers selected' in result.output

    def test_status_command(self):
        """Test status command."""
        runner = CliRunner()
        result = runner.invoke(cli, ['status'])

        assert result.exit_code == 0
        assert 'Data Directory Status' in result.output

    def test_update_bellingham_crime_flag_works(self):
        """Test that --bellingham-crime flag is recognized."""
        runner = CliRunner()
        result = runner.invoke(cli, ['update', '--bellingham-crime', '--help'])

        # Should show help without error
        assert result.exit_code == 0
        assert 'Update data from web sources' in result.output

    def test_update_seattle_crime_flag_works(self):
        """Test that --seattle-crime flag is recognized."""
        runner = CliRunner()
        result = runner.invoke(cli, ['update', '--seattle-crime', '--help'])

        # Should show help without error
        assert result.exit_code == 0
        assert 'Update data from web sources' in result.output

    @patch('src.data.cli.SCRAPER_CLASSES', {'test_scraper': Mock})
    @patch('src.data.cli.ConfigManager')
    def test_update_all_enabled_scrapers(self, mock_config_manager):
        """Test updating all enabled scrapers."""
        # Mock config
        mock_config = Mock()
        mock_config.get.return_value = {
            'level': 'INFO',
            'file': 'logs/scraper.log'
        }
        mock_config.get_all_scrapers.return_value = {
            'test_scraper': {
                'enabled': True,
                'name': 'Test Scraper'
            },
            'disabled_scraper': {
                'enabled': False,
                'name': 'Disabled Scraper'
            }
        }
        mock_config.get_scraper_config.return_value = {
            'name': 'Test Scraper',
            'output_file': 'test.csv',
            'output_dir': 'raw'
        }
        mock_config_manager.return_value = mock_config

        # Mock scraper
        mock_scraper = Mock()
        mock_scraper.run.return_value = True

        with patch('src.data.cli.SCRAPER_CLASSES', {'test_scraper': Mock(return_value=mock_scraper)}):
            runner = CliRunner()
            result = runner.invoke(cli, ['update', '--all'])

            # Should only run enabled scraper
            assert result.exit_code == 0
            assert 'test_scraper' in result.output

    @patch('src.data.cli.ConfigManager')
    def test_update_scraper_failure(self, mock_config_manager):
        """Test handling of scraper failure."""
        # Mock config
        mock_config = Mock()
        mock_config.get.return_value = {
            'level': 'INFO',
            'file': 'logs/scraper.log'
        }
        mock_config.get_scraper_config.return_value = {
            'name': 'Failing Scraper',
            'output_file': 'test.csv',
            'output_dir': 'raw'
        }
        mock_config_manager.return_value = mock_config

        # Mock scraper that fails
        mock_scraper = Mock()
        mock_scraper.run.return_value = False

        with patch('src.data.cli.BellinghamCrimeScraper', return_value=mock_scraper):
            runner = CliRunner()
            result = runner.invoke(cli, ['update', '--bellingham-crime'])

            assert result.exit_code == 0
            assert 'failed' in result.output

    def test_update_with_custom_config(self, tmp_path):
        """Test update with custom config file."""
        # Create temp config
        config_file = tmp_path / "custom_config.yaml"
        config_file.write_text("""
project:
  name: test

data_dirs:
  raw: data/1_raw

logging:
  level: INFO
  file: logs/test.log

scrapers:
  test_scraper:
    enabled: true
    name: Test
""")

        runner = CliRunner()
        result = runner.invoke(cli, ['update', '--config', str(config_file)])

        # Should not crash with custom config
        assert 'No scrapers selected' in result.output or result.exit_code == 0

    def test_update_with_log_level(self):
        """Test update with different log levels."""
        runner = CliRunner()

        # Test each log level
        for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
            result = runner.invoke(cli, ['update', '--log-level', level])
            # Should accept the log level without error
            assert 'No scrapers selected' in result.output or result.exit_code == 0
