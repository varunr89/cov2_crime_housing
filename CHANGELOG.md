# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2025-11-06

### Added
- Unified CLI tool for web scraping (`python -m src.data.cli`)
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
  - `update` - Update data from sources
  - `status` - Check data file status
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
