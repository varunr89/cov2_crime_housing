COV2_CrimeRate
==============================

Effect of COV2 on crime rate in cities of Bellingham and Seattle in Western Washington.
Stretch Goal: Merge dataset with City of Bellingham Housing sale data, develop sale price ML model and quantitatively evaluate the impact of crime on property sale price on a block level. 

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── 0_external       <- Data from third party sources.
    │   ├── 2_interim        <- Intermediate data that has been transformed.
    │   │   ├── Bellingham_Property_Sale_Combined.csv 	<- All Residential Property Sale data in Bellingham between 2015 and 2021.
    │   │   ├── COB_CrimeReport.csv   			<- All Police activity detail in City of Bellingham between 2015 and 2021. 
    │   ├── 3_processed      <- The final, canonical data sets for modeling.
    │   │   ├── Bellingham_Property_Sale_Clean.csv 	<- Residential Property Sales Data cleaned and prepared for machine learning.
    │   │   ├── Cleaned_Merged_Housing_Crime_Data.csv 	<- Cleaned Residential Property Sales data merged with Crime Data.
    │   │   ├── MachineLearing_X_beforeFE.csv 		<- Input for Machine Learning models (not feature engineering) with monthly time-series.
    │   │   ├── MachineLearing_y_beforeFE.csv 		<- target for Machine Learning models (not feature engineering) with monthly time-series.
    │   └── 1_raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │      ├── CrimeData_EDA.ipynb 	<- Explore Bellingham Police Activity Scanner
    │      ├── HousingData_EDA.ipynb  	<- Explore Housing data. Merge with Crime data. Train Models.                    
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   ├── WhatcomCtyProperty_serialScraper_.py 	<- Serial Scrapper to scrape Whatcom Assesors Properties
    │   │   ├── WhatcomCtyProperty_parallelScraper.py   <- Parallelized Scrapper to scrape Whatcom Assesors Properties
    │   │   ├── WhatcomCtyAss_Scraper.py        	<- Scrapper to scrape Whatcom Assesors Sale Search output
    │   │   ├── COB_PoliceActivity_Scraper.py        	<- Scrape Bellingham Police Activity Scanner
    │   │   ├── make_dataset.py        			<- Download data from Seattle PD activity
    │   │   ├── helper_functions.py        		<- helper functions for scraping
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


Summary of Results
==============================

1. <p><small> Medium blog post <a target="_blank" href="https://capcloudcoder.medium.com/impact-of-cov-2-on-local-crime-statistics-ea8154294d22">Impact of COV-2 on local crime statistics</a>. #datascience #Webscraping #aspnet #covid19 #crime</small></p>

References
==============================

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
