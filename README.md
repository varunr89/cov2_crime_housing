# COVID-19 Crime and Housing Analysis

This project analyzes how COVID-19 affected crime rates in Bellingham and Seattle, Washington. The analysis uses property sales data to quantify crime's impact on housing prices at the block level.

## Quick Start

Install dependencies:

```bash
pip install -e .
```

Update all data sources:

```bash
python -m src.data.cli update --all
```

Check data status:

```bash
python -m src.data.cli status
```

See [docs/SCRAPER_CLI.md](docs/SCRAPER_CLI.md) for complete CLI documentation.

## Project Structure

```
├── data/                    # Data pipeline
│   ├── 0_external/          # Third-party sources
│   ├── 1_raw/               # Original downloads
│   ├── 2_interim/           # Transformed data
│   └── 3_processed/         # Analysis-ready datasets
├── src/data/                # Unified web scraper CLI
│   ├── cli.py               # Main CLI interface
│   ├── config.yaml          # Scraper configuration
│   ├── scrapers/            # Scraper implementations
│   └── utils/               # Logging and helpers
├── notebooks/               # Jupyter analysis notebooks
├── models/                  # Trained ML models
└── tests/                   # Test suite
```

## Key Features

The unified CLI scraper provides:

- **Automated data collection** from three sources: Bellingham police reports, Seattle crime API, and Whatcom County property sales
- **Retry logic** with exponential backoff for failed requests
- **Rate limiting** to respect server resources
- **YAML configuration** for all scraper settings
- **Comprehensive logging** with automatic rotation

## Data Sources

**Bellingham Crime Data**
- Source: City of Bellingham Police Activity Scanner
- Coverage: 2015-2024
- Output: `data/2_interim/COB_CrimeReport.csv`

**Seattle Crime Data**
- Source: Seattle Open Data API
- Coverage: Complete historical dataset
- Output: `data/1_raw/Seattle_Crime_Data.csv`

**Property Sales Data**
- Source: Whatcom County Assessor
- Coverage: Bellingham residential sales
- Output: `data/2_interim/Bellingham_Property_Part1.csv`

## Analysis Notebooks

**CrimeData_EDA.ipynb** explores 139,487 crime records from Bellingham police activity.

**HousingData_EDA.ipynb** merges housing and crime data, then trains ML models to quantify crime's impact on property prices.

## Development

Run tests:

```bash
pytest tests/data/ -v
```

Add a new scraper:

1. Inherit from `BaseScraper` in `src/data/scrapers/base_scraper.py`
2. Implement the `scrape()` method
3. Register in `SCRAPER_CLASSES` dictionary (`src/data/cli.py`)
4. Add configuration to `src/data/config.yaml`
5. Write tests in `tests/data/scrapers/`

## Results

Read the [Medium analysis](https://capcloudcoder.medium.com/impact-of-cov-2-on-local-crime-statistics-ea8154294d22) of COVID-19's impact on local crime statistics.

## Credits

Project structure follows the [cookiecutter data science template](https://drivendata.github.io/cookiecutter-data-science/).
