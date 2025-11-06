import pytest
from unittest.mock import Mock, patch, MagicMock
from src.data.utils.selenium_helper import create_driver, quit_driver


class TestSeleniumHelper:
    """Test Selenium helper utilities."""

    @patch('src.data.utils.selenium_helper.webdriver.Chrome')
    @patch('src.data.utils.selenium_helper.ChromeDriverManager')
    def test_create_driver_default_options(self, mock_manager, mock_chrome):
        """Test creating driver with default options."""
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        mock_manager.return_value.install.return_value = '/path/to/driver'

        driver = create_driver()

        assert driver == mock_driver
        mock_chrome.assert_called_once()

    @patch('src.data.utils.selenium_helper.webdriver.Chrome')
    @patch('src.data.utils.selenium_helper.ChromeDriverManager')
    def test_create_driver_headless(self, mock_manager, mock_chrome):
        """Test creating driver in headless mode."""
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        mock_manager.return_value.install.return_value = '/path/to/driver'

        driver = create_driver(headless=True)

        # Verify Chrome was called with options
        assert mock_chrome.called
        call_kwargs = mock_chrome.call_args.kwargs
        assert 'options' in call_kwargs

    @patch('src.data.utils.selenium_helper.webdriver.Chrome')
    @patch('src.data.utils.selenium_helper.ChromeDriverManager')
    def test_create_driver_custom_options(self, mock_manager, mock_chrome):
        """Test creating driver with custom options."""
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        mock_manager.return_value.install.return_value = '/path/to/driver'

        custom_opts = ['--window-size=1920,1080', '--disable-notifications']
        driver = create_driver(options=custom_opts)

        assert driver == mock_driver

    def test_quit_driver(self):
        """Test quitting driver safely."""
        mock_driver = Mock()

        quit_driver(mock_driver)

        mock_driver.quit.assert_called_once()

    def test_quit_driver_handles_none(self):
        """Test quitting None driver doesn't raise error."""
        # Should not raise exception
        quit_driver(None)

    def test_quit_driver_handles_exception(self):
        """Test quitting driver handles exceptions gracefully."""
        mock_driver = Mock()
        mock_driver.quit.side_effect = Exception("Driver error")

        # Should not raise exception
        quit_driver(mock_driver)
