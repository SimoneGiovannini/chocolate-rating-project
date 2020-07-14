import pandas as pd

countries = pd.read_excel('./country_data.xlsx')
countries = countries[['Region Name', 'Sub-region Name', 'Country or Area']]
countries.columns = ['Continent', 'Sub-region', 'Country']

# Add Taiwan
countries = pd.concat([countries, pd.DataFrame([['Asia', 'Eastern Asia', 'Taiwan']], columns=countries.columns)], ignore_index=True)

countries['Country'] = countries['Country'].str.replace('United States of America', 'U.S.A.')
countries['Country'] = countries['Country'].str.replace('Russian Federation', 'Russia')
countries['Country'] = countries['Country'].str.replace('United Kingdom of Great Britain and Northern Ireland', 'U.K.')
countries['Country'] = countries['Country'].str.replace('Viet Nam', 'Vietnam')
countries['Country'] = countries['Country'].str.replace('Venezuela (Bolivarian Republic of)', 'Venezuela', regex=False)
countries['Country'] = countries['Country'].str.replace('Republic of Korea', 'South Korea')
countries['Country'] = countries['Country'].str.replace('Sao Tome and Principe', 'Sao Tome')
countries['Country'] = countries['Country'].str.replace('Saint Lucia', 'St. Lucia')
countries['Country'] = countries['Country'].str.replace('Bolivia (Plurinational State of)', 'Bolivia', regex=False)
countries['Country'] = countries['Country'].str.replace('Saint Vincent and the Grenadines', 'St.Vincent-Grenadines')
countries['Country'] = countries['Country'].str.replace('Czechia', 'Czech Republic')
countries['Country'] = countries['Country'].str.replace('United Arab Emirates', 'U.A.E.')
countries['Country'] = countries['Country'].str.replace('United Republic of Tanzania', 'Tanzania')
countries['Country'] = countries['Country'].str.replace('Democratic Republic of the Congo', 'DR Congo')
countries['Country'] = countries['Country'].str.replace('Côte d’Ivoire', 'Ivory Coast')
countries['Country'] = countries['Country'].str.replace('Myanmar', 'Burma')

countries.to_csv('./countries.csv', index=False)