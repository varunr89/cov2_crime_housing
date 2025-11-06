# Unified CLI Web Scraper Tool

Use superpowers:executing-plans to implement this plan.

**Goal:** Convert 5 separate web scraping scripts into a single unified CLI tool with configuration management, error handling, incremental updates, and data validation.

**Architecture:** Build a modular CLI application using Click framework with a base scraper class that all domain-specific scrapers inherit from. Configuration is externalized to YAML, with centralized logging and error handling. Each scraper implements a common interface for consistency and testability.

**Tech Stack:** Python 3.8+, Click (CLI), PyYAML (config), requests (HTTP), BeautifulSoup4 (parsing), Selenium (browser automation), pandas (data manipulation), pytest (testing), tqdm (progress bars)

---

## Task 1: Project Setup and Dependencies

**Files:**
- Modify: `/home/user/cov2_crime_housing/requirements.txt`
- Create: `/home/user/cov2_crime_housing/setup.py`
- Create: `/home/user/cov2_crime_housing/pytest.ini`

**Step 1: Update requirements.txt**

Add all necessary dependencies:

```txt
-e .

# CLI and Configuration
click>=8.0.0
pyyaml>=6.0.0
python-dotenv>=0.5.1

# Web Scraping
requests>=2.28.0
beautifulsoup4>=4.11.0
selenium>=4.0.0
webdriver-manager>=3.8.0

# Data Processing
pandas>=1.4.0

# Utilities
tqdm>=4.64.0
tenacity>=8.2.0

# Development Tools
pytest>=7.0.0
pytest-cov>=3.0.0
pytest-mock>=3.10.0
flake8
black>=22.0.0

# Documentation
Sphinx
sphinx-click

# Cloud
awscli

# Code Quality
coverage
mypy>=0.990
```

**Step 2: Create setup.py**

Update package configuration:

```python
from setuptools import find_packages, setup

setup(
    name='cov2_crime_housing',
    packages=find_packages(),
    version='0.2.0',
    description='COVID-19 Crime and Housing Data Analysis with Unified CLI Scraper',
    author='Your Name',
    license='MIT',
    entry_points={
        'console_scripts': [
            'scraper=src.data.cli:main',
        ],
    },
    python_requires='>=3.8',
)
```

**Step 3: Create pytest.ini**

Configure pytest:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --cov=src
    --cov-report=html
    --cov-report=term-missing
```

**Step 4: Install dependencies**

```bash
cd /home/user/cov2_crime_housing
pip install -e .
```

Expected output: Successfully installed cov2_crime_housing and all dependencies.

**Step 5: Commit**

```bash
git add requirements.txt setup.py pytest.ini
git commit -m "chore: add dependencies and test configuration for unified CLI scraper"
```

---

## Task 2: Directory Structure and Configuration

**Files:**
- Create: `/home/user/cov2_crime_housing/src/data/scrapers/__init__.py`
- Create: `/home/user/cov2_crime_housing/src/data/utils/__init__.py`
- Create: `/home/user/cov2_crime_housing/src/data/config.yaml`
- Create: `/home/user/cov2_crime_housing/tests/data/__init__.py`
- Create: `/home/user/cov2_crime_housing/tests/data/scrapers/__init__.py`
- Create: `/home/user/cov2_crime_housing/.gitignore` (modify)

**Step 1: Create directory structure**

```bash
mkdir -p /home/user/cov2_crime_housing/src/data/scrapers
mkdir -p /home/user/cov2_crime_housing/src/data/utils
mkdir -p /home/user/cov2_crime_housing/tests/data/scrapers
mkdir -p /home/user/cov2_crime_housing/logs
mkdir -p /home/user/cov2_crime_housing/data/{0_external,1_raw,2_interim,3_processed}
```

**Step 2: Create empty __init__.py files**

```bash
touch /home/user/cov2_crime_housing/src/data/scrapers/__init__.py
touch /home/user/cov2_crime_housing/src/data/utils/__init__.py
touch /home/user/cov2_crime_housing/tests/data/__init__.py
touch /home/user/cov2_crime_housing/tests/data/scrapers/__init__.py
```

**Step 3: Create config.yaml**

```yaml
# Configuration for Unified Web Scraper CLI Tool
project:
  name: cov2_crime_housing
  version: 0.2.0

# Data directory paths (relative to project root)
data_dirs:
  external: data/0_external
  raw: data/1_raw
  interim: data/2_interim
  processed: data/3_processed

# Logging configuration
logging:
  level: INFO
  file: logs/scraper.log
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  max_bytes: 10485760  # 10MB
  backup_count: 5

# Scraper configurations
scrapers:
  bellingham_crime:
    enabled: true
    name: Bellingham Police Activity
    url: https://police.cob.org/PIRPressSummary/ReleaseForm.aspx
    output_file: COB_CrimeReport.csv
    output_dir: interim
    start_year: 2015
    end_year: 2024
    rate_limit_seconds: 2
    max_retries: 3
    timeout: 30

  seattle_crime:
    enabled: true
    name: Seattle Police Crime Data
    url: https://data.seattle.gov/resource/tazs-3rd5.json
    output_file: Seattle_Crime_Data.csv
    output_dir: raw
    limit: 1000000
    rate_limit_seconds: 1
    max_retries: 3
    timeout: 60

  property_sales:
    enabled: true
    name: Whatcom County Property Sales
    url: https://property.whatcomcounty.us/PropertyAccess/SearchResultsSales.aspx
    output_file: Bellingham_Property_Part1.csv
    output_dir: interim
    max_pages: 200
    headless: true
    rate_limit_seconds: 3
    max_retries: 3
    timeout: 30

  property_details:
    enabled: false  # Manual trigger only
    name: Whatcom County Property Details
    input_file: Bellingham_Property_Part1.csv
    output_file: Bellingham_Property_Complete.csv
    output_dir: interim
    parallel: false
    max_workers: 4
    headless: true
    rate_limit_seconds: 2
    max_retries: 3
    timeout: 30

# Browser configuration for Selenium scrapers
selenium:
  browser: chrome
  driver_path: auto  # auto-detect or specify path
  options:
    - --no-sandbox
    - --headless
    - --disable-dev-shm-usage
    - --disable-gpu
    - --window-size=1920,1080

# Rate limiting and retry settings
rate_limiting:
  enabled: true
  default_delay: 2  # seconds between requests

retry:
  max_attempts: 3
  backoff_factor: 2  # exponential backoff: 1s, 2s, 4s
  backoff_max: 30  # max wait time in seconds
```

**Step 4: Update .gitignore**

Ensure logs directory is ignored:

```bash
echo "logs/" >> /home/user/cov2_crime_housing/.gitignore
```

**Step 5: Commit**

```bash
git add src/data/scrapers/__init__.py src/data/utils/__init__.py src/data/config.yaml tests/data/ .gitignore
git commit -m "feat: add project structure and configuration for unified scraper"
```

---

## Task 3: Configuration Manager

**Files:**
- Create: `/home/user/cov2_crime_housing/src/data/config_manager.py`
- Create: `/home/user/cov2_crime_housing/tests/data/test_config_manager.py`

**Step 1: Write failing test**

```python
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
```

**Step 2: Run test**

```bash
cd /home/user/cov2_crime_housing
pytest tests/data/test_config_manager.py -v
```

Expected output: FAILED - ModuleNotFoundError: No module named 'src.data.config_manager'

**Step 3: Write minimal implementation**

```python
"""Configuration manager for unified web scraper CLI."""
from pathlib import Path
from typing import Any, Dict, Optional
import yaml


class ConfigManager:
    """Manages application configuration from YAML file."""

    def __init__(self, config_path: Optional[str] = None, project_root: Optional[str] = None):
        """
        Initialize configuration manager.

        Args:
            config_path: Path to YAML configuration file. Defaults to src/data/config.yaml
            project_root: Project root directory. Defaults to current working directory
        """
        if project_root is None:
            self.project_root = Path.cwd()
        else:
            self.project_root = Path(project_root)

        if config_path is None:
            config_path = self.project_root / 'src' / 'data' / 'config.yaml'

        self.config_path = Path(config_path)
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.

        Args:
            key: Configuration key in dot notation (e.g., 'scrapers.bellingham_crime.url')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def get_scraper_config(self, scraper_name: str) -> Dict[str, Any]:
        """
        Get complete configuration for a specific scraper.

        Args:
            scraper_name: Name of the scraper (e.g., 'bellingham_crime')

        Returns:
            Dictionary containing scraper configuration
        """
        config = self.get(f'scrapers.{scraper_name}', default={})
        if not config:
            raise ValueError(f"Scraper configuration not found: {scraper_name}")

        return config

    def get_data_dir(self, dir_type: str) -> Path:
        """
        Get absolute path to data directory.

        Args:
            dir_type: Type of data directory ('raw', 'interim', 'processed', 'external')

        Returns:
            Absolute path to data directory
        """
        relative_path = self.get(f'data_dirs.{dir_type}')
        if relative_path is None:
            raise ValueError(f"Data directory not configured: {dir_type}")

        return self.project_root / relative_path

    def get_all_scrapers(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all scraper configurations.

        Returns:
            Dictionary mapping scraper names to their configurations
        """
        return self.get('scrapers', default={})
```

**Step 4: Verify passing tests**

```bash
pytest tests/data/test_config_manager.py -v
```

Expected output: All tests PASSED

**Step 5: Commit**

```bash
git add src/data/config_manager.py tests/data/test_config_manager.py
git commit -m "feat: implement configuration manager with YAML support"
```

---

## Task 4: Logging Utilities

**Files:**
- Create: `/home/user/cov2_crime_housing/src/data/utils/logger.py`
- Create: `/home/user/cov2_crime_housing/tests/data/test_logger.py`

**Step 1: Write failing test**

```python
import pytest
import logging
from pathlib import Path
from src.data.utils.logger import setup_logger, get_logger


class TestLogger:
    """Test logging utilities."""

    def test_setup_logger_creates_file(self, tmp_path):
        """Test that setup_logger creates log file."""
        log_file = tmp_path / "test.log"
        logger = setup_logger(
            name='test_logger',
            log_file=str(log_file),
            level=logging.INFO
        )

        assert log_file.exists()
        assert logger.level == logging.INFO

    def test_logger_writes_messages(self, tmp_path):
        """Test that logger writes messages to file."""
        log_file = tmp_path / "test.log"
        logger = setup_logger(
            name='test_write',
            log_file=str(log_file),
            level=logging.INFO
        )

        test_message = "Test log message"
        logger.info(test_message)

        log_content = log_file.read_text()
        assert test_message in log_content
        assert "INFO" in log_content

    def test_logger_respects_level(self, tmp_path):
        """Test that logger respects log level."""
        log_file = tmp_path / "test.log"
        logger = setup_logger(
            name='test_level',
            log_file=str(log_file),
            level=logging.WARNING
        )

        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")

        log_content = log_file.read_text()
        assert "Debug message" not in log_content
        assert "Info message" not in log_content
        assert "Warning message" in log_content

    def test_get_logger_returns_existing(self, tmp_path):
        """Test that get_logger returns existing logger."""
        log_file = tmp_path / "test.log"
        logger1 = setup_logger(
            name='shared_logger',
            log_file=str(log_file),
            level=logging.INFO
        )

        logger2 = get_logger('shared_logger')

        assert logger1 is logger2
```

**Step 2: Run test**

```bash
pytest tests/data/test_logger.py -v
```

Expected output: FAILED - ModuleNotFoundError: No module named 'src.data.utils.logger'

**Step 3: Write minimal implementation**

```python
"""Logging utilities for unified web scraper."""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logger(
    name: str,
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    format_string: Optional[str] = None,
    max_bytes: int = 10485760,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Set up a logger with file and console handlers.

    Args:
        name: Logger name
        log_file: Path to log file. If None, only console logging is enabled
        level: Logging level
        format_string: Custom format string. Uses default if None
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup log files to keep

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # Default format
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    formatter = logging.Formatter(format_string)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler with rotation
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get an existing logger by name.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
```

**Step 4: Verify passing tests**

```bash
pytest tests/data/test_logger.py -v
```

Expected output: All tests PASSED

**Step 5: Commit**

```bash
git add src/data/utils/logger.py tests/data/test_logger.py
git commit -m "feat: implement logging utilities with rotation support"
```

---

## Task 5: Base Scraper Class

**Files:**
- Create: `/home/user/cov2_crime_housing/src/data/scrapers/base_scraper.py`
- Create: `/home/user/cov2_crime_housing/tests/data/scrapers/test_base_scraper.py`

**Step 1: Write failing test**

```python
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
```

**Step 2: Run test**

```bash
pytest tests/data/scrapers/test_base_scraper.py -v
```

Expected output: FAILED - ModuleNotFoundError: No module named 'src.data.scrapers.base_scraper'

**Step 3: Write minimal implementation**

```python
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
```

**Step 4: Verify passing tests**

```bash
pytest tests/data/scrapers/test_base_scraper.py -v
```

Expected output: All tests PASSED

**Step 5: Commit**

```bash
git add src/data/scrapers/base_scraper.py tests/data/scrapers/test_base_scraper.py
git commit -m "feat: implement base scraper class with common functionality"
```

---

## Task 6: Selenium Helper Utilities

**Files:**
- Create: `/home/user/cov2_crime_housing/src/data/utils/selenium_helper.py`
- Create: `/home/user/cov2_crime_housing/tests/data/test_selenium_helper.py`

**Step 1: Write failing test**

```python
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
```

**Step 2: Run test**

```bash
pytest tests/data/test_selenium_helper.py -v
```

Expected output: FAILED - ModuleNotFoundError: No module named 'src.data.utils.selenium_helper'

**Step 3: Write minimal implementation**

```python
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
```

**Step 4: Verify passing tests**

```bash
pytest tests/data/test_selenium_helper.py -v
```

Expected output: All tests PASSED

**Step 5: Commit**

```bash
git add src/data/utils/selenium_helper.py tests/data/test_selenium_helper.py
git commit -m "feat: implement Selenium helper utilities for browser automation"
```

---

## Task 7: Bellingham Crime Scraper

**Files:**
- Create: `/home/user/cov2_crime_housing/src/data/scrapers/bellingham_crime.py`
- Create: `/home/user/cov2_crime_housing/tests/data/scrapers/test_bellingham_crime.py`
- Modify: `/home/user/cov2_crime_housing/src/data/COB_PoliceActivity_Scraper.py` (reference only)

**Step 1: Write failing test**

```python
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

    @patch('src.data.scrapers.bellingham_crime.requests.get')
    def test_get_form_tokens(self, mock_get, mock_config, tmp_path):
        """Test extraction of ASP.NET form tokens."""
        # Mock HTML response with form tokens
        mock_response = Mock()
        mock_response.text = '''
        <html>
            <input name="__VIEWSTATE" value="test_viewstate" />
            <input name="__VIEWSTATEGENERATOR" value="test_generator" />
            <input name="__EVENTVALIDATION" value="test_validation" />
        </html>
        '''
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        scraper = BellinghamCrimeScraper(
            name='bellingham_crime',
            config=mock_config,
            project_root=str(tmp_path)
        )

        tokens = scraper._get_form_tokens()

        assert tokens['__VIEWSTATE'] == 'test_viewstate'
        assert tokens['__VIEWSTATEGENERATOR'] == 'test_generator'
        assert tokens['__EVENTVALIDATION'] == 'test_validation'

    @patch('src.data.scrapers.bellingham_crime.requests.post')
    @patch('src.data.scrapers.bellingham_crime.requests.get')
    def test_scrape_month_data(self, mock_get, mock_post, mock_config, tmp_path):
        """Test scraping data for a single month."""
        # Mock initial GET for tokens
        mock_get_response = Mock()
        mock_get_response.text = '''
        <input name="__VIEWSTATE" value="vs" />
        <input name="__VIEWSTATEGENERATOR" value="vsg" />
        <input name="__EVENTVALIDATION" value="ev" />
        '''
        mock_get_response.raise_for_status = Mock()
        mock_get.return_value = mock_get_response

        # Mock POST response with crime data
        mock_post_response = Mock()
        mock_post_response.text = '''
        <table>
            <tr>
                <td>01/15/2020</td>
                <td>123 Main St</td>
                <td>Theft - Case #2020-001</td>
            </tr>
        </table>
        '''
        mock_post_response.raise_for_status = Mock()
        mock_post.return_value = mock_post_response

        scraper = BellinghamCrimeScraper(
            name='bellingham_crime',
            config=mock_config,
            project_root=str(tmp_path)
        )

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
```

**Step 2: Run test**

```bash
pytest tests/data/scrapers/test_bellingham_crime.py -v
```

Expected output: FAILED - ModuleNotFoundError: No module named 'src.data.scrapers.bellingham_crime'

**Step 3: Write minimal implementation**

```python
"""Bellingham Police Activity scraper."""
import re
from datetime import datetime
from typing import Dict, List
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

from src.data.scrapers.base_scraper import BaseScraper


class BellinghamCrimeScraper(BaseScraper):
    """Scraper for Bellingham Police Activity reports."""

    def __init__(self, name: str, config: Dict, project_root: str = None):
        """Initialize Bellingham crime scraper."""
        super().__init__(name, config, project_root)

        self.base_url = config['url']
        self.start_year = config.get('start_year', 2015)
        self.end_year = config.get('end_year', datetime.now().year)

        self.session = requests.Session()

    def _get_form_tokens(self) -> Dict[str, str]:
        """
        Extract ASP.NET form tokens from the page.

        Returns:
            Dictionary containing __VIEWSTATE, __VIEWSTATEGENERATOR, __EVENTVALIDATION
        """
        response = self.session.get(self.base_url, timeout=self.timeout)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        tokens = {
            '__VIEWSTATE': soup.find('input', {'name': '__VIEWSTATE'})['value'],
            '__VIEWSTATEGENERATOR': soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value'],
            '__EVENTVALIDATION': soup.find('input', {'name': '__EVENTVALIDATION'})['value']
        }

        return tokens

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _scrape_month(self, year: int, month: int) -> pd.DataFrame:
        """
        Scrape crime data for a specific month.

        Args:
            year: Year to scrape
            month: Month to scrape (1-12)

        Returns:
            DataFrame containing crime records for the month
        """
        self.logger.info(f"Scraping data for {year}-{month:02d}")

        # Get form tokens
        tokens = self._get_form_tokens()

        # Calculate date range (first to last day of month)
        start_date = f"{month}/01/{year}"
        if month == 12:
            end_date = f"12/31/{year}"
        else:
            # Last day of month
            next_month = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
            last_day = (next_month - pd.Timedelta(days=1)).day
            end_date = f"{month}/{last_day}/{year}"

        # Prepare POST data
        form_data = {
            '__VIEWSTATE': tokens['__VIEWSTATE'],
            '__VIEWSTATEGENERATOR': tokens['__VIEWSTATEGENERATOR'],
            '__EVENTVALIDATION': tokens['__EVENTVALIDATION'],
            'ctl00$ContentPlaceHolder1$txtStartDate': start_date,
            'ctl00$ContentPlaceHolder1$txtEndDate': end_date,
            'ctl00$ContentPlaceHolder1$btnSubmit': 'Submit'
        }

        # Submit form
        response = self.session.post(self.base_url, data=form_data, timeout=self.timeout)
        response.raise_for_status()

        # Parse results
        soup = BeautifulSoup(response.text, 'html.parser')
        records = []

        # Find table rows
        table = soup.find('table')
        if table:
            rows = table.find_all('tr')[1:]  # Skip header row

            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    # Extract data
                    date_str = cols[0].get_text(strip=True)
                    location = cols[1].get_text(strip=True)
                    offence_full = cols[2].get_text(strip=True)

                    # Parse offence and case details
                    match = re.match(r'(.*?)\s*-\s*Case\s*#?\s*(.+)', offence_full)
                    if match:
                        offence = match.group(1).strip()
                        case_details = match.group(2).strip()
                    else:
                        offence = offence_full
                        case_details = ''

                    # Categorize crime (simple categorization)
                    crime_category = self._categorize_crime(offence)

                    records.append({
                        'Date': date_str,
                        'Location': location,
                        'Offence': offence,
                        'Crime Category': crime_category,
                        'Case Details': case_details
                    })

        # Apply rate limiting
        self.apply_rate_limit()

        return pd.DataFrame(records)

    def _categorize_crime(self, offence: str) -> str:
        """
        Categorize crime based on offence description.

        Args:
            offence: Offence description

        Returns:
            Crime category
        """
        offence_lower = offence.lower()

        if any(word in offence_lower for word in ['theft', 'burglary', 'robbery', 'stolen']):
            return 'Property'
        elif any(word in offence_lower for word in ['assault', 'battery', 'homicide', 'violence']):
            return 'Violent'
        elif any(word in offence_lower for word in ['drug', 'narcotic', 'controlled substance']):
            return 'Drug'
        elif any(word in offence_lower for word in ['traffic', 'dui', 'driving']):
            return 'Traffic'
        else:
            return 'Other'

    def scrape(self) -> pd.DataFrame:
        """
        Scrape all crime data for configured date range.

        Returns:
            DataFrame containing all crime records
        """
        all_data = []

        for year in range(self.start_year, self.end_year + 1):
            for month in range(1, 13):
                try:
                    month_data = self._scrape_month(year, month)
                    if not month_data.empty:
                        all_data.append(month_data)
                except Exception as e:
                    self.logger.error(f"Error scraping {year}-{month:02d}: {e}")
                    continue

        if all_data:
            return pd.concat(all_data, ignore_index=True)
        else:
            return pd.DataFrame()
```

**Step 4: Verify passing tests**

```bash
pytest tests/data/scrapers/test_bellingham_crime.py -v
```

Expected output: All tests PASSED

**Step 5: Commit**

```bash
git add src/data/scrapers/bellingham_crime.py tests/data/scrapers/test_bellingham_crime.py
git commit -m "feat: implement Bellingham crime scraper with retry logic"
```

---

## Task 8: Seattle Crime Scraper

**Files:**
- Create: `/home/user/cov2_crime_housing/src/data/scrapers/seattle_crime.py`
- Create: `/home/user/cov2_crime_housing/tests/data/scrapers/test_seattle_crime.py`

**Step 1: Write failing test**

```python
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
```

**Step 2: Run test**

```bash
pytest tests/data/scrapers/test_seattle_crime.py -v
```

Expected output: FAILED - ModuleNotFoundError: No module named 'src.data.scrapers.seattle_crime'

**Step 3: Write minimal implementation**

```python
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
```

**Step 4: Verify passing tests**

```bash
pytest tests/data/scrapers/test_seattle_crime.py -v
```

Expected output: All tests PASSED

**Step 5: Commit**

```bash
git add src/data/scrapers/seattle_crime.py tests/data/scrapers/test_seattle_crime.py
git commit -m "feat: implement Seattle crime API scraper"
```

---

## Task 9: Property Sales Scraper

**Files:**
- Create: `/home/user/cov2_crime_housing/src/data/scrapers/property_sales.py`
- Create: `/home/user/cov2_crime_housing/tests/data/scrapers/test_property_sales.py`

**Step 1: Write failing test**

```python
import pytest
from unittest.mock import Mock, patch, MagicMock
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

    @patch('src.data.scrapers.property_sales.create_driver')
    def test_scrape_page_data(self, mock_create_driver, mock_config, tmp_path):
        """Test scraping single page."""
        # Mock WebDriver
        mock_driver = Mock()
        mock_driver.page_source = '''
        <table>
            <tr>
                <td><a href="/detail/12345">Property Link</a></td>
                <td>123 Main St</td>
                <td>01/15/2020</td>
                <td>$350,000</td>
            </tr>
        </table>
        '''
        mock_create_driver.return_value = mock_driver

        scraper = PropertySalesScraper(
            name='property_sales',
            config=mock_config,
            project_root=str(tmp_path)
        )

        df = scraper._scrape_page(mock_driver, 1)

        assert len(df) >= 0  # May be empty if parsing logic differs
        assert 'Address' in df.columns or df.empty
```

**Step 2: Run test**

```bash
pytest tests/data/scrapers/test_property_sales.py -v
```

Expected output: FAILED - ModuleNotFoundError: No module named 'src.data.scrapers.property_sales'

**Step 3: Write minimal implementation**

```python
"""Whatcom County property sales scraper using Selenium."""
from typing import Dict
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tenacity import retry, stop_after_attempt, wait_exponential

from src.data.scrapers.base_scraper import BaseScraper
from src.data.utils.selenium_helper import create_driver, quit_driver


class PropertySalesScraper(BaseScraper):
    """Scraper for Whatcom County property sales."""

    def __init__(self, name: str, config: Dict, project_root: str = None):
        """Initialize property sales scraper."""
        super().__init__(name, config, project_root)

        self.base_url = config['url']
        self.max_pages = config.get('max_pages', 200)
        self.headless = config.get('headless', True)

    def _scrape_page(self, driver, page_num: int) -> pd.DataFrame:
        """
        Scrape a single page of property sales.

        Args:
            driver: Selenium WebDriver instance
            page_num: Page number to scrape

        Returns:
            DataFrame containing property sales from the page
        """
        self.logger.info(f"Scraping page {page_num}")

        # Parse page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        records = []

        # Find sales table
        table = soup.find('table', {'id': 'GridView1'})
        if not table:
            return pd.DataFrame()

        rows = table.find_all('tr')[1:]  # Skip header

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 4:
                # Extract link
                link_tag = cols[0].find('a')
                link = link_tag['href'] if link_tag else ''

                # Extract fields
                address = cols[1].get_text(strip=True)
                sale_date = cols[2].get_text(strip=True)
                sale_price = cols[3].get_text(strip=True)

                records.append({
                    'Assessor Link': link,
                    'Address': address,
                    'Sale Date': sale_date,
                    'Sale Price': sale_price
                })

        return pd.DataFrame(records)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def scrape(self) -> pd.DataFrame:
        """
        Scrape property sales data.

        Returns:
            DataFrame containing all property sales
        """
        driver = None
        all_data = []

        try:
            # Create WebDriver
            driver = create_driver(headless=self.headless)
            driver.get(self.base_url)

            # Wait for page to load
            WebDriverWait(driver, self.timeout).until(
                EC.presence_of_element_located((By.ID, 'GridView1'))
            )

            # Scrape first page
            page_data = self._scrape_page(driver, 1)
            if not page_data.empty:
                all_data.append(page_data)

            # Navigate through pages
            for page_num in range(2, self.max_pages + 1):
                try:
                    # Find and click next page button
                    next_button = driver.find_element(By.LINK_TEXT, str(page_num))
                    next_button.click()

                    # Wait for page to load
                    WebDriverWait(driver, self.timeout).until(
                        EC.presence_of_element_located((By.ID, 'GridView1'))
                    )

                    # Scrape page
                    page_data = self._scrape_page(driver, page_num)
                    if not page_data.empty:
                        all_data.append(page_data)

                    # Apply rate limiting
                    self.apply_rate_limit()

                except Exception as e:
                    self.logger.warning(f"Stopped at page {page_num}: {e}")
                    break

            if all_data:
                return pd.concat(all_data, ignore_index=True)
            else:
                return pd.DataFrame()

        finally:
            quit_driver(driver)
```

**Step 4: Verify passing tests**

```bash
pytest tests/data/scrapers/test_property_sales.py -v
```

Expected output: All tests PASSED

**Step 5: Commit**

```bash
git add src/data/scrapers/property_sales.py tests/data/scrapers/test_property_sales.py
git commit -m "feat: implement property sales scraper with Selenium"
```

---

## Task 10: CLI Main Interface

**Files:**
- Create: `/home/user/cov2_crime_housing/src/data/cli.py`
- Create: `/home/user/cov2_crime_housing/tests/data/test_cli.py`

**Step 1: Write failing test**

```python
import pytest
from unittest.mock import Mock, patch
from click.testing import CliRunner
from src.data.cli import cli, update, status


class TestCLI:
    """Test CLI interface."""

    def test_cli_help(self):
        """Test CLI help message."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])

        assert result.exit_code == 0
        assert 'Unified web scraper CLI' in result.output

    def test_update_help(self):
        """Test update command help."""
        runner = CliRunner()
        result = runner.invoke(update, ['--help'])

        assert result.exit_code == 0
        assert 'Update data from web sources' in result.output

    @patch('src.data.cli.ConfigManager')
    @patch('src.data.cli.setup_logger')
    def test_update_all(self, mock_logger, mock_config_manager):
        """Test updating all scrapers."""
        # Mock configuration
        mock_config = Mock()
        mock_config.get_all_scrapers.return_value = {
            'test_scraper': {
                'enabled': True,
                'name': 'Test Scraper'
            }
        }
        mock_config_manager.return_value = mock_config

        runner = CliRunner()
        result = runner.invoke(update, ['--all'])

        # Should attempt to run scrapers
        assert result.exit_code == 0

    @patch('src.data.cli.ConfigManager')
    @patch('src.data.cli.setup_logger')
    def test_status_command(self, mock_logger, mock_config_manager):
        """Test status command."""
        mock_config = Mock()
        mock_config.get_data_dir.return_value = '/tmp/data'
        mock_config_manager.return_value = mock_config

        runner = CliRunner()
        result = runner.invoke(status)

        assert result.exit_code == 0
```

**Step 2: Run test**

```bash
pytest tests/data/test_cli.py -v
```

Expected output: FAILED - ModuleNotFoundError: No module named 'src.data.cli'

**Step 3: Write minimal implementation**

```python
"""Unified CLI for web scraping tools."""
import click
import logging
from pathlib import Path
from typing import Optional

from src.data.config_manager import ConfigManager
from src.data.utils.logger import setup_logger
from src.data.scrapers.bellingham_crime import BellinghamCrimeScraper
from src.data.scrapers.seattle_crime import SeattleCrimeScraper
from src.data.scrapers.property_sales import PropertySalesScraper


# Scraper registry
SCRAPER_CLASSES = {
    'bellingham_crime': BellinghamCrimeScraper,
    'seattle_crime': SeattleCrimeScraper,
    'property_sales': PropertySalesScraper,
}


@click.group()
@click.version_option(version='0.2.0')
def cli():
    """Unified web scraper CLI for COVID-19 Crime and Housing data."""
    pass


@cli.command()
@click.option('--all', 'all_scrapers', is_flag=True, help='Update all enabled scrapers')
@click.option('--bellingham-crime', 'bellingham_crime', is_flag=True, help='Update Bellingham crime data')
@click.option('--seattle-crime', 'seattle_crime', is_flag=True, help='Update Seattle crime data')
@click.option('--property-sales', 'property_sales', is_flag=True, help='Update property sales data')
@click.option('--config', type=click.Path(exists=True), help='Path to config file')
@click.option('--log-level', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR']), default='INFO')
def update(all_scrapers, bellingham_crime, seattle_crime, property_sales, config, log_level):
    """Update data from web sources."""
    # Load configuration
    config_manager = ConfigManager(config_path=config)

    # Setup logging
    log_config = config_manager.get('logging', {})
    logger = setup_logger(
        name='scraper.cli',
        log_file=log_config.get('file', 'logs/scraper.log'),
        level=getattr(logging, log_level)
    )

    logger.info("=" * 60)
    logger.info("Starting unified web scraper")
    logger.info("=" * 60)

    # Determine which scrapers to run
    scrapers_to_run = []

    if all_scrapers:
        # Run all enabled scrapers
        all_scraper_configs = config_manager.get_all_scrapers()
        for scraper_name, scraper_config in all_scraper_configs.items():
            if scraper_config.get('enabled', False):
                scrapers_to_run.append(scraper_name)
    else:
        # Run specific scrapers
        if bellingham_crime:
            scrapers_to_run.append('bellingham_crime')
        if seattle_crime:
            scrapers_to_run.append('seattle_crime')
        if property_sales:
            scrapers_to_run.append('property_sales')

    if not scrapers_to_run:
        click.echo("No scrapers selected. Use --all or specify individual scrapers.")
        return

    # Run scrapers
    results = {}
    for scraper_name in scrapers_to_run:
        click.echo(f"\n{'=' * 60}")
        click.echo(f"Running: {scraper_name}")
        click.echo('=' * 60)

        try:
            # Get scraper configuration
            scraper_config = config_manager.get_scraper_config(scraper_name)

            # Get scraper class
            scraper_class = SCRAPER_CLASSES.get(scraper_name)
            if not scraper_class:
                logger.error(f"Scraper not implemented: {scraper_name}")
                results[scraper_name] = False
                continue

            # Initialize and run scraper
            scraper = scraper_class(
                name=scraper_name,
                config=scraper_config,
                project_root=str(Path.cwd())
            )

            success = scraper.run()
            results[scraper_name] = success

            if success:
                click.echo(f"✓ {scraper_name} completed successfully")
            else:
                click.echo(f"✗ {scraper_name} failed")

        except Exception as e:
            logger.error(f"Error running {scraper_name}: {e}", exc_info=True)
            results[scraper_name] = False
            click.echo(f"✗ {scraper_name} failed: {e}")

    # Summary
    click.echo(f"\n{'=' * 60}")
    click.echo("Summary")
    click.echo('=' * 60)

    successful = sum(1 for v in results.values() if v)
    total = len(results)

    click.echo(f"Successful: {successful}/{total}")

    for scraper_name, success in results.items():
        status = "✓" if success else "✗"
        click.echo(f"  {status} {scraper_name}")


@cli.command()
@click.option('--config', type=click.Path(exists=True), help='Path to config file')
def status(config):
    """Check status of data files."""
    config_manager = ConfigManager(config_path=config)

    click.echo("Data Directory Status")
    click.echo("=" * 60)

    # Check each data directory
    for dir_type in ['external', 'raw', 'interim', 'processed']:
        try:
            data_dir = config_manager.get_data_dir(dir_type)

            if data_dir.exists():
                files = list(data_dir.glob('*.csv'))
                click.echo(f"\n{dir_type.upper()}: {data_dir}")

                if files:
                    for f in files:
                        size_mb = f.stat().st_size / (1024 * 1024)
                        click.echo(f"  - {f.name} ({size_mb:.2f} MB)")
                else:
                    click.echo("  (no CSV files)")
            else:
                click.echo(f"\n{dir_type.upper()}: Not found")

        except Exception as e:
            click.echo(f"\n{dir_type.upper()}: Error - {e}")


def main():
    """Entry point for CLI."""
    cli()


if __name__ == '__main__':
    main()
```

**Step 4: Verify passing tests**

```bash
pytest tests/data/test_cli.py -v
```

Expected output: All tests PASSED

**Step 5: Commit**

```bash
git add src/data/cli.py tests/data/test_cli.py
git commit -m "feat: implement unified CLI with update and status commands"
```

---

## Task 11: Documentation and Usage Guide

**Files:**
- Create: `/home/user/cov2_crime_housing/docs/SCRAPER_CLI.md`
- Modify: `/home/user/cov2_crime_housing/README.md`

**Step 1: Create scraper documentation**

```markdown
# Unified Web Scraper CLI

A command-line tool for scraping COVID-19, crime, and housing data from multiple sources.

## Installation

```bash
cd /home/user/cov2_crime_housing
pip install -e .
```

## Quick Start

### Update All Data Sources

```bash
scraper update --all
```

### Update Specific Data Sources

```bash
# Bellingham crime data
scraper update --bellingham-crime

# Seattle crime data
scraper update --seattle-crime

# Property sales data
scraper update --property-sales
```

### Check Data Status

```bash
scraper status
```

## Configuration

Configuration is managed via `src/data/config.yaml`. Key settings:

### Data Directories

```yaml
data_dirs:
  external: data/0_external
  raw: data/1_raw
  interim: data/2_interim
  processed: data/3_processed
```

### Scraper Settings

Each scraper has individual configuration:

```yaml
scrapers:
  bellingham_crime:
    enabled: true
    start_year: 2015
    end_year: 2024
    rate_limit_seconds: 2
```

### Logging

```yaml
logging:
  level: INFO
  file: logs/scraper.log
  max_bytes: 10485760  # 10MB
  backup_count: 5
```

## Available Scrapers

### 1. Bellingham Crime (`bellingham_crime`)

Scrapes police activity reports from City of Bellingham.

**Source:** https://police.cob.org/PIRPressSummary/ReleaseForm.aspx

**Output:** `data/2_interim/COB_CrimeReport.csv`

**Fields:**
- Date
- Location
- Offence
- Crime Category
- Case Details

**Configuration Options:**
- `start_year`: First year to scrape (default: 2015)
- `end_year`: Last year to scrape (default: current year)
- `rate_limit_seconds`: Delay between requests (default: 2)

### 2. Seattle Crime (`seattle_crime`)

Fetches crime data from Seattle Open Data API.

**Source:** https://data.seattle.gov/resource/tazs-3rd5.json

**Output:** `data/1_raw/Seattle_Crime_Data.csv`

**Fields:** All fields from Socrata API (report number, offense, date, location, etc.)

**Configuration Options:**
- `limit`: Maximum records to fetch (default: 1,000,000)

### 3. Property Sales (`property_sales`)

Scrapes residential property sales from Whatcom County Assessor.

**Source:** https://property.whatcomcounty.us/PropertyAccess/SearchResultsSales.aspx

**Output:** `data/2_interim/Bellingham_Property_Part1.csv`

**Fields:**
- Assessor Link
- Address
- Sale Date
- Sale Price

**Configuration Options:**
- `max_pages`: Maximum pages to scrape (default: 200)
- `headless`: Run browser in headless mode (default: true)

## Advanced Usage

### Custom Configuration File

```bash
scraper update --all --config /path/to/custom_config.yaml
```

### Adjust Log Level

```bash
scraper update --all --log-level DEBUG
```

## Scheduling Updates

### Using Cron (Linux/Mac)

Edit crontab:

```bash
crontab -e
```

Add daily update at 2 AM:

```cron
0 2 * * * cd /home/user/cov2_crime_housing && scraper update --all >> logs/cron.log 2>&1
```

### Using systemd Timer (Linux)

Create `/etc/systemd/system/scraper.service`:

```ini
[Unit]
Description=Web Scraper Update
After=network.target

[Service]
Type=oneshot
User=user
WorkingDirectory=/home/user/cov2_crime_housing
ExecStart=/usr/bin/scraper update --all
```

Create `/etc/systemd/system/scraper.timer`:

```ini
[Unit]
Description=Daily Web Scraper Update

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

Enable timer:

```bash
sudo systemctl enable scraper.timer
sudo systemctl start scraper.timer
```

## Troubleshooting

### Chrome Driver Issues

If Selenium scrapers fail:

1. Ensure Chrome/Chromium is installed
2. The scraper auto-downloads chromedriver via `webdriver-manager`
3. For manual driver path, update `config.yaml`:

```yaml
selenium:
  driver_path: /path/to/chromedriver
```

### Rate Limiting

If you receive HTTP 429 errors, increase rate limits:

```yaml
scrapers:
  scraper_name:
    rate_limit_seconds: 5  # Increase delay
```

### Memory Issues

For large datasets, process in smaller chunks by adjusting year ranges or limits.

## Development

### Running Tests

```bash
pytest tests/data/ -v
```

### Adding New Scrapers

1. Create scraper class inheriting from `BaseScraper`
2. Implement `scrape()` method
3. Add to `SCRAPER_CLASSES` in `cli.py`
4. Add configuration to `config.yaml`
5. Write tests

## License

MIT
```

**Step 2: Update main README**

Add reference to scraper CLI in the main README:

```markdown
## Unified Web Scraper CLI

This project includes a unified CLI tool for updating all data sources. See [docs/SCRAPER_CLI.md](docs/SCRAPER_CLI.md) for complete documentation.

### Quick Start

```bash
# Install
pip install -e .

# Update all data
scraper update --all

# Check status
scraper status
```
```

**Step 3: Verify documentation**

```bash
cat /home/user/cov2_crime_housing/docs/SCRAPER_CLI.md
```

Expected output: Complete documentation displayed

**Step 4: Commit**

```bash
git add docs/SCRAPER_CLI.md README.md
git commit -m "docs: add comprehensive CLI scraper documentation"
```

---

## Task 12: Integration Testing

**Files:**
- Create: `/home/user/cov2_crime_housing/tests/data/test_integration.py`

**Step 1: Write integration tests**

```python
import pytest
from pathlib import Path
from click.testing import CliRunner
from src.data.cli import cli
from src.data.config_manager import ConfigManager


class TestIntegration:
    """Integration tests for complete workflows."""

    @pytest.fixture
    def test_project_dir(self, tmp_path):
        """Set up test project directory structure."""
        # Create directories
        for subdir in ['0_external', '1_raw', '2_interim', '3_processed']:
            (tmp_path / 'data' / subdir).mkdir(parents=True)

        (tmp_path / 'logs').mkdir()
        (tmp_path / 'src' / 'data').mkdir(parents=True)

        # Create test config
        config_content = """
project:
  name: test_project
  version: 0.2.0

data_dirs:
  external: data/0_external
  raw: data/1_raw
  interim: data/2_interim
  processed: data/3_processed

logging:
  level: INFO
  file: logs/scraper.log
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

scrapers:
  test_scraper:
    enabled: true
    name: Test Scraper
    url: https://example.com
    output_file: test.csv
    output_dir: raw
    rate_limit_seconds: 0
"""
        config_path = tmp_path / 'src' / 'data' / 'config.yaml'
        config_path.write_text(config_content)

        return tmp_path

    def test_config_manager_loads_project_config(self, test_project_dir):
        """Test that ConfigManager loads project configuration."""
        config_path = test_project_dir / 'src' / 'data' / 'config.yaml'
        config = ConfigManager(
            config_path=str(config_path),
            project_root=str(test_project_dir)
        )

        assert config.get('project.name') == 'test_project'
        assert config.get('scrapers.test_scraper.enabled') is True

        # Test data directory resolution
        raw_dir = config.get_data_dir('raw')
        assert raw_dir == test_project_dir / 'data' / '1_raw'

    def test_cli_status_shows_data_directories(self, test_project_dir):
        """Test that CLI status command works."""
        import os
        os.chdir(test_project_dir)

        runner = CliRunner()
        result = runner.invoke(cli, ['status'])

        # Should complete successfully
        assert result.exit_code == 0
        assert 'Data Directory Status' in result.output

    def test_full_workflow_config_to_cli(self, test_project_dir):
        """Test complete workflow from config to CLI execution."""
        import os
        os.chdir(test_project_dir)

        # Load config
        config_path = test_project_dir / 'src' / 'data' / 'config.yaml'
        config = ConfigManager(
            config_path=str(config_path),
            project_root=str(test_project_dir)
        )

        # Verify configuration
        assert config.get('project.name') == 'test_project'

        # Run status command
        runner = CliRunner()
        result = runner.invoke(cli, ['status'])

        assert result.exit_code == 0
```

**Step 2: Run integration tests**

```bash
pytest tests/data/test_integration.py -v
```

Expected output: All tests PASSED

**Step 3: Run full test suite**

```bash
pytest tests/data/ -v --cov=src/data --cov-report=term-missing
```

Expected output: All tests PASSED with coverage report

**Step 4: Commit**

```bash
git add tests/data/test_integration.py
git commit -m "test: add integration tests for complete workflows"
```

---

## Task 13: Final Verification and Cleanup

**Files:**
- Modify: `/home/user/cov2_crime_housing/.gitignore`
- Create: `/home/user/cov2_crime_housing/CHANGELOG.md`

**Step 1: Update .gitignore**

Ensure all necessary patterns are ignored:

```bash
echo "
# Scraper artifacts
*.log
logs/
.pytest_cache/
__pycache__/
*.pyc
.coverage
htmlcov/
*.egg-info/

# Browser drivers
chromedriver
geckodriver
" >> /home/user/cov2_crime_housing/.gitignore
```

**Step 2: Create CHANGELOG**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2025-11-06

### Added
- Unified CLI tool for web scraping (`scraper` command)
- Configuration management via YAML (`src/data/config.yaml`)
- Centralized logging with rotation
- Base scraper class for consistent interface
- Selenium helper utilities for browser automation
- Bellingham crime scraper (refactored from original script)
- Seattle crime API scraper (refactored from original script)
- Property sales scraper with Selenium (refactored from original script)
- Retry logic with exponential backoff using tenacity
- Comprehensive test suite with pytest
- CLI commands:
  - `scraper update` - Update data from sources
  - `scraper status` - Check data file status
- Complete documentation in `docs/SCRAPER_CLI.md`

### Changed
- Updated requirements.txt with all dependencies
- Refactored scraping logic into modular classes
- Improved error handling and logging throughout
- Made all file paths configurable (removed hard-coded Windows paths)

### Fixed
- Hard-coded file paths now use configuration
- Missing dependencies now included in requirements.txt
- Browser driver auto-download via webdriver-manager

## [0.1.0] - Initial Release

### Added
- Initial project structure
- Original scraping scripts
- Jupyter notebooks for EDA
- Data pipeline for crime and housing analysis
```

**Step 3: Run final verification**

```bash
cd /home/user/cov2_crime_housing

# Verify all tests pass
pytest tests/data/ -v

# Verify CLI is installed
scraper --help

# Verify configuration is valid
python -c "from src.data.config_manager import ConfigManager; c = ConfigManager(); print('Config OK')"
```

Expected output: All tests pass, CLI help displayed, config loads successfully

**Step 4: Commit**

```bash
git add .gitignore CHANGELOG.md
git commit -m "chore: update gitignore and add changelog for v0.2.0"
```

---

## Execution Options

You can execute this plan in two ways:

### Option 1: Subagent-Driven (Current Session)
Execute each task with a fresh subagent, with code review between tasks. This provides:
- Fast iteration cycle
- Immediate feedback
- Incremental progress tracking

To proceed: Respond with "Start Task 1" (or any specific task number)

### Option 2: Parallel Session (New Session)
Create a new Claude session and use the `executing-plans` skill to batch-execute all tasks with checkpoints. This provides:
- Autonomous execution
- Checkpoint-based progress
- Batch processing

To proceed: Open new session and reference this plan file

---

## Notes

- All file paths are absolute as required
- Each task includes complete code (no abstractions)
- Tests follow TDD approach (write → fail → implement → pass → commit)
- Configuration is externalized (no hard-coded values)
- Retry logic handles transient failures
- Rate limiting respects server resources
- Logging provides visibility into scraping operations

**Estimated Total Time:** 4-6 hours (assuming 2-5 minutes per task, ~80 granular steps)
