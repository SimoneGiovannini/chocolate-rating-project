from bs4 import BeautifulSoup
import requests
import pandas as pd

# Parse data from http://flavorsofcacao.com/database_w_REF.html
# Code from https://srome.github.io/Parsing-HTML-Tables-in-Python-with-BeautifulSoup-and-pandas/

class HTMLTableParser:
       
    def parse_url(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        return [(table['id'],self.parse_html_table(table))\
                for table in soup.find_all('table')]  

    def parse_html_table(self, table):
        n_columns = 0
        n_rows=0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can
        for row in table.find_all('tr'):
            
            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows+=1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)
                    
            # Handle column names if we find them
            th_tags = row.find_all('th') 
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())

        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0,n_columns)
        df = pd.DataFrame(columns = columns,
                          index= range(0,n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                content = column.get_text().strip()
                #Convert blank cells to null
                try:
                    if content.strip() == '':
                        content = None
                except:
                    pass
                df.iat[row_marker,column_marker] = content
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1
                
        # Convert to float if possible
        for col in df:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass
        
        return df


url = "http://flavorsofcacao.com/database_w_REF.html"
hp = HTMLTableParser()
df = hp.parse_url(url)[0][1]

# Remove % symbol from Cocoa Percent and convert to float
df['Cocoa Percent'] = df['Cocoa Percent'].str.replace('%', '').astype('float')

# Join dataset with country data to get continent and sub-region
# Country data taken from https://unstats.un.org/unsd/methodology/m49/

# Change some country names to match names from country dataset
df['Company Location'] = df['Company Location'].str.replace('Sao Tome & Principe', 'Sao Tome')
df['Company Location'] = df['Company Location'].str.replace('Amsterdam', 'Netherlands')
df['Company Location'] = df['Company Location'].str.replace('Scotland|Wales', 'U.K.')
df['Country of Bean Origin'] = df['Country of Bean Origin'].str.replace('Sao Tome & Principe|^Principe', 'Sao Tome')
df['Country of Bean Origin'] = df['Country of Bean Origin'].str.replace('Trinidad$|^Tobago', 'Trinidad and Tobago')
df['Country of Bean Origin'] = df['Country of Bean Origin'].str.replace('Sumatra|Sulawesi', 'Indonesia')
df['Country of Bean Origin'] = df['Country of Bean Origin'].str.replace('Bolvia', 'Bolivia')
df['Country of Bean Origin'] = df['Country of Bean Origin'].str.replace('blend', 'Blend')

# Get continent and sub-region of Company Location
df = df.merge(countries.rename(lambda s: s+'_comp_loc', axis=1), 
              how='left', 
              right_on='Country_comp_loc', 
              left_on='Company Location').drop('Country_comp_loc', axis=1)

# Get continent and sub-region of Country of Bean Origin
df = df.merge(countries.rename(lambda s: s+'_origin', axis=1), 
              how='left', 
              right_on='Country_origin', 
              left_on='Country of Bean Origin').drop('Country_origin', axis=1)

# Fill data for blends
df = df.fillna({'Continent_origin':'Blend', 'Sub-region_origin':'Blend', 'Country_origin':'Blend'})

df.to_csv('./dataset.csv', index=False)
