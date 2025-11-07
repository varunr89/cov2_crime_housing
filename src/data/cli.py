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
