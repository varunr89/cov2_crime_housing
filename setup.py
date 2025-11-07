from setuptools import find_packages, setup

setup(
    name='cov2_crime_housing',
    packages=find_packages(),
    version='0.2.0',
    description='COVID-19 Crime and Housing Data Analysis with Unified CLI Scraper',
    author='capcloudcoder',
    license='MIT',
    entry_points={
        'console_scripts': [
            'scraper=src.data.cli:main',
        ],
    },
    python_requires='>=3.8',
)
