import sys
# import libraries
import pandas as pd 
import numpy
import re
from sqlalchemy import create_engine
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline ,FeatureUnion
from sklearn.feature_extraction.text import CountVectorizer ,TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier ,AdaBoostClassifier
from sklearn.model_selection import train_test_split , GridSearchCV
from sklearn.metrics import classification_report
import pickle
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
stopWords=set(stopwords.words('english'))
def load_data(database_filepath):
    """
    load data from database    
    Arguments:
        database_filepath -> database file path 
    Outputs:
        X -> X is message 
        Y -> Y is the catgoryes
        cloumn name -> catgoryes names
    """
    engine = create_engine(f'sqlite:///{database_filepath}')
    df = pd.read_sql_table('data',engine)
    X = df.iloc[:,1]
    Y = df.iloc[:,4:40]
    return X,Y, Y.columns

def tokenize(text):
    """
    tokenize data from raw text    
    Arguments:
        text -> raw text 
    Outputs:
        words -> list of tokenized word
    """
    text=text.lower()
    text = re.sub(r'[^a-zA-Z0-9]' ,' ',text)
    token=word_tokenize(text)
    lemmatizer= WordNetLemmatizer() 
    words=[]
    for word in token:
        if word not in stopWords:
            word=lemmatizer.lemmatize(word)
            words.append(word)
    
    return words


def build_model():
    """
    build pipeline to predect the catgoryes of message    
    Outputs:
        model -> model to predect the catgoryes of message 
    """
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)), 
        ('tfidf' , TfidfTransformer()),
        ('clv', MultiOutputClassifier(RandomForestClassifier()))
            ])
    parameters = {
   
    'clv__estimator__max_features': ['auto', 'sqrt'],
    'clv__estimator__min_samples_leaf':[2,4,6],
    'clv__estimator__min_samples_split':[3,6,15],
         }
    
    cv = GridSearchCV(pipeline,param_grid=parameters)
    return cv

def evaluate_model(model, X_test, Y_test, category_names):
    
    """
        evaluateing model to model show Preformance     
        Arguments:
            model -> database file path 
            X_test -> test feature 
            Y_test -> test target  
    """
    Y_predect=model.predict(X_test)
    for category in range(len(category_names)):
        print('--------------------------------------------------')
        print(Y_test.columns[category],':')
        print(classification_report(Y_test.iloc[:,category],Y_predect[:,category],target_names=Y_test.columns[category]))
        print('--------------------------------------------------')
        


def save_model(model, model_filepath):
    """
        save model into pickle extension   
        Arguments:
        model -> model to be saved 
        model_filepath ->  file path that model will be saved to   
    """
    pickle.dump(model ,open(model_filepath,'wb'))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()