# Web Scraper CLI

This CLI scrapes crime and housing data from Bellingham, Seattle, and Whatcom County.

## Installation

```bash
cd /home/user/cov2_crime_housing
pip install -e .
```

## Commands

### Update Data

Update all enabled scrapers:

```bash
python -m src.data.cli update --all
```

Update specific scrapers:

```bash
python -m src.data.cli update --bellingham-crime
python -m src.data.cli update --seattle-crime
python -m src.data.cli update --property-sales
```

Set log level:

```bash
python -m src.data.cli update --all --log-level DEBUG
```

Use custom configuration:

```bash
python -m src.data.cli update --all --config /path/to/config.yaml
```

### Check Status

View data directory status:

```bash
python -m src.data.cli status
```

## Configuration

Edit `src/data/config.yaml` to configure scrapers.

### Data Directories

```yaml
data_dirs:
  external: data/0_external
  raw: data/1_raw
  interim: data/2_interim
  processed: data/3_processed
```

### Logging

```yaml
logging:
  level: INFO
  file: logs/scraper.log
  max_bytes: 10485760  # 10MB
  backup_count: 5
```

### Scraper Settings

Each scraper accepts these options:

```yaml
scrapers:
  bellingham_crime:
    enabled: true
    start_year: 2015
    end_year: 2024
    rate_limit_seconds: 2
```

## Scrapers

### Bellingham Crime

**Data:** Police activity reports from City of Bellingham

**Source:** https://police.cob.org/PIRPressSummary/ReleaseForm.aspx

**Output:** `data/2_interim/COB_CrimeReport.csv`

**Fields:**
- Date
- Location
- Offence
- Crime Category
- Case Details

**Options:**
- `start_year` — First year to scrape (default: 2015)
- `end_year` — Last year to scrape (default: current year)
- `rate_limit_seconds` — Delay between requests (default: 2)

### Seattle Crime

**Data:** Crime reports from Seattle Open Data API

**Source:** https://data.seattle.gov/resource/tazs-3rd5.json

**Output:** `data/1_raw/Seattle_Crime_Data.csv`

**Fields:** All Socrata API fields (report number, offense, date, location, coordinates)

**Options:**
- `limit` — Maximum records to fetch (default: 1,000,000)

### Property Sales

**Data:** Residential property sales from Whatcom County Assessor

**Source:** https://property.whatcomcounty.us/PropertyAccess/SearchResultsSales.aspx

**Output:** `data/2_interim/Bellingham_Property_Part1.csv`

**Fields:**
- Assessor Link
- Address
- Sale Date
- Sale Price

**Options:**
- `max_pages` — Maximum pages to scrape (default: 200)
- `headless` — Run browser without display (default: true)

## Scheduling

### Cron (Linux/Mac)

Run daily at 2 AM:

```bash
crontab -e
```

Add:

```cron
0 2 * * * cd /home/user/cov2_crime_housing && python -m src.data.cli update --all >> logs/cron.log 2>&1
```

### systemd (Linux)

Create `/etc/systemd/system/scraper.service`:

```ini
[Unit]
Description=Web Scraper Update
After=network.target

[Service]
Type=oneshot
User=user
WorkingDirectory=/home/user/cov2_crime_housing
ExecStart=/usr/bin/python -m src.data.cli update --all
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

Enable:

```bash
sudo systemctl enable scraper.timer
sudo systemctl start scraper.timer
```

## Troubleshooting

### Chrome Driver Issues

The scraper auto-downloads chromedriver via `webdriver-manager`. Install Chrome if missing:

```bash
# Ubuntu/Debian
sudo apt-get install chromium-browser

# macOS
brew install --cask google-chrome
```

Specify driver path in `config.yaml`:

```yaml
selenium:
  driver_path: /path/to/chromedriver
```

### Rate Limiting

Increase delays if you receive HTTP 429 errors:

```yaml
scrapers:
  scraper_name:
    rate_limit_seconds: 5
```

### Memory Issues

Process large datasets in smaller chunks by adjusting year ranges or limits in configuration.

## Development

### Run Tests

```bash
pytest tests/data/ -v
```

### Add Scraper

1. Create class in `src/data/scrapers/` that inherits from `BaseScraper`
2. Implement `scrape()` method returning a pandas DataFrame
3. Register in `SCRAPER_CLASSES` dictionary in `src/data/cli.py`
4. Add configuration block to `src/data/config.yaml`
5. Write tests in `tests/data/scrapers/test_your_scraper.py`

Example:

```python
from src.data.scrapers.base_scraper import BaseScraper
import pandas as pd

class YourScraper(BaseScraper):
    def scrape(self) -> pd.DataFrame:
        # Your scraping logic
        return df
```

## License

MIT
