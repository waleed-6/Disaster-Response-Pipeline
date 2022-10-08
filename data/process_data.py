import sys
import pandas as pd
import re
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
        """
        load Data into dataframe 
    
         Arguments:
            messages_filepath -> file path for messages 
            categories_filepath -> file path for categories 
        Outputs:
        df -> load messages and categories into dataframe 
        """
        messages = pd.read_csv(messages_filepath)
        categories = pd.read_csv(categories_filepath)
        df = messages.merge(categories,how='inner', on = 'id')
        return df


def clean_data(df):
    
    """
    Clean Data    
    Arguments:
        df -> raw data dataframe
    Outputs:
        df -> cleaned data  dataframe
    """
        
    categories = df['categories'].str.split(';',expand=True)
    row = categories[:1]
    category_colnames=[]
    for r in row.values[0]:
        s=re.sub('[^A-Za-z_]+', '', r)
        category_colnames.append(s)
    categories.columns = category_colnames
    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].astype(str)
        categories[column] = categories[column].str[-1:] 
        categories = categories[categories!=2]
        # convert column from string to numeric
        categories[column] = categories[column].astype(int)
    df = df.drop('categories',axis=1)
    df = pd.concat((df,categories) ,axis=1 )
    df = df.drop_duplicates()
    return df


def save_data(df, database_filename):
    
    """
    Save data     
    Arguments:
        df -> cleaned data  dataframe
       database_filename -> database file path 
    """
    engine = create_engine(f'sqlite:///{database_filename}')
    df.to_sql('data', engine, index=False, if_exists='replace')


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()