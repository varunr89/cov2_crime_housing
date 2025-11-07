"""Selenium helper utilities for browser automation."""
from typing import List, Optional
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)


def create_driver(
    headless: bool = True,
    options: Optional[List[str]] = None,
    driver_path: Optional[str] = None
) -> webdriver.Chrome:
    """
    Create and configure a Chrome WebDriver instance.

    Args:
        headless: Run browser in headless mode
        options: List of additional Chrome options
        driver_path: Path to chromedriver. If None, auto-downloads

    Returns:
        Configured Chrome WebDriver instance
    """
    chrome_options = Options()

    # Default options
    default_options = [
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu'
    ]

    if headless:
        default_options.append('--headless')

    # Apply default options
    for option in default_options:
        chrome_options.add_argument(option)

    # Apply custom options
    if options:
        for option in options:
            chrome_options.add_argument(option)

    # Set up driver service
    if driver_path and driver_path != 'auto':
        service = Service(executable_path=driver_path)
    else:
        # Auto-download driver
        service = Service(ChromeDriverManager().install())

    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logger.info("Chrome WebDriver created successfully")
        return driver
    except Exception as e:
        logger.error(f"Failed to create Chrome WebDriver: {e}")
        raise


def quit_driver(driver: Optional[webdriver.Chrome]) -> None:
    """
    Safely quit a WebDriver instance.

    Args:
        driver: WebDriver instance to quit
    """
    if driver is None:
        return

    try:
        driver.quit()
        logger.info("WebDriver quit successfully")
    except Exception as e:
        logger.warning(f"Error quitting WebDriver: {e}")
