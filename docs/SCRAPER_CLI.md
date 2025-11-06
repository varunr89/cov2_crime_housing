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
python -m src.data.cli update --all
```

### Update Specific Data Sources

```bash
# Bellingham crime data
python -m src.data.cli update --bellingham-crime

# Seattle crime data
python -m src.data.cli update --seattle-crime

# Property sales data
python -m src.data.cli update --property-sales
```

### Check Data Status

```bash
python -m src.data.cli status
```

## Configuration

Configuration is managed via `src/data/config.yaml`. Key settings include data directories, logging, and scraper-specific settings like date ranges and rate limits.

## Available Scrapers

### 1. Bellingham Crime (`bellingham_crime`)
- **Source:** City of Bellingham Police Activity reports
- **Output:** `data/2_interim/COB_CrimeReport.csv`
- **Configurable:** start_year, end_year, rate_limit_seconds

### 2. Seattle Crime (`seattle_crime`)
- **Source:** Seattle Open Data API
- **Output:** `data/1_raw/Seattle_Crime_Data.csv`
- **Configurable:** limit (max records)

### 3. Property Sales (`property_sales`)
- **Source:** Whatcom County Assessor
- **Output:** `data/2_interim/Bellingham_Property_Part1.csv`
- **Configurable:** max_pages, headless mode

## Scheduling Updates

### Using Cron (Linux/Mac)

```cron
0 2 * * * cd /home/user/cov2_crime_housing && python -m src.data.cli update --all >> logs/cron.log 2>&1
```

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
