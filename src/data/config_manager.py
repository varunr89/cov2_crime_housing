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
