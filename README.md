# Chocolate rating project
## Overview
- Analyzed a dataset of over 2300 chocolate bars' ratings scraped from http://flavorsofcacao.com/.
- Enriched the dataset with additional data about countries of bean origin and location of companies.
- Analyzed data distributions using multiple visualizations.
- Used feature engineering to encode variables such as Ingredients and Most Memorable Characteristics.
- Trained Linear Regression, Ridge Regression, SVM and CatBoost models to predict the rating of bars.
- Examined the CatBoost model to determined which features have most impact in predicting ratings.

## Data Collection

The data was taken from http://flavorsofcacao.com(last update on March 14, 2020). See also <a href="https://www.kaggle.com/rtatman/chocolate-bar-ratings">this Kaggle dataset</a> for an outdated version of the same data.

- The dataset was scraped from the HTML table http://flavorsofcacao.com/chocolate_database.html using BeautifulSoup. Some of the scraping code was taken from https://srome.github.io/Parsing-HTML-Tables-in-Python-with-BeautifulSoup-and-pandas/.

- In the original database each bar is described by the following features:
  - REF
  - Company (Manufacturer)
  - Company Location
  - Review Date
  - Country of Bean Origin
  - Specific Bean Origin or Bar Name
  - Cocoa Percent
  - Ingredients
  - Most Memorable Characteristics
  - Rating

- We enriched these features by adding the continent and sub-region of both Company Location and Country of Bean Origin. This was done by joining the table with geographical data taken from https://unstats.un.org/unsd/methodology/m49/.

- Company (Manufacturer) was parsed to get two distinct features for Company and Manufacturer.

## Exploratory Data Analysis

We analyzed the dataset by creating lots of visualizations and tables. The following are some examples.

- Soma is the top rated company among those which got more than 10 reviews:
![Top rated Company Locations](top_rated.png)

Here are boxplots of rating distributions for the companies with most reviews:
![Rating distribution by Company](company_ratings.png)

- Most companies are located in Northern America:
![Rating distribution by Company](company_locations.png)

while most of the cocoa beans have origin from Latin America and the Caribbean:
![Rating distribution by Company](origin_regions.png)

[work in progress]
