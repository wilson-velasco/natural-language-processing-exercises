import unicodedata
import re
import json
import nltk

import pandas as pd

import acquire

from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

def basic_clean(string):
    lower_string = string.lower()
    
    normal_string = unicodedata.normalize('NFKD', lower_string)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
    
    normal_no_chars_string = re.sub(r'[^a-z0-9\s]', '', normal_string.replace("'", " "))
    
    return normal_no_chars_string

def tokenize(string):
    ttt = ToktokTokenizer()
    return ttt.tokenize(string, return_str=True)

def stem(string):
    ps = nltk.porter.PorterStemmer()
    
    stems = [ps.stem(word) for word in string.split()]

    stemmed_string = ' '.join(stems)
    
    return stemmed_string

def lemmatize(string):
    wnl = nltk.stem.WordNetLemmatizer()
    
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    
    lemmed_string = ' '.join(lemmas)
    
    return lemmed_string

def remove_stopwords(string, extra_words=[], exclude_words=[]):
    stopword_list = stopwords.words('english')
    
    #Removing words from list
    stopword_list = [word for word in stopword_list if word not in exclude_words]
    
    #Adding words to list
    
    for word in extra_words:
        stopword_list.append(word)
    
    no_stop_words = [word for word in string.split() if word not in stopword_list]
    
    no_stop_string = ' '.join(no_stop_words)
    
    return no_stop_string

def parse_df(df, title='title', content='content'):
    '''Takes in a dataframe with title and content columns and returns a df with title,
    original content, and content as it appears cleaned, stemmed, and lemmatized.'''

    new_df = pd.DataFrame()

    new_df['title'] = df[title]
    new_df['original'] = df[content]
    new_df['clean'] = [remove_stopwords(tokenize(basic_clean(string))) for string in df[content]]
    new_df['stemmed'] = [stem(string) for string in new_df.clean]
    new_df['lemmatized'] = [lemmatize(string) for string in new_df.clean]

    return new_df

