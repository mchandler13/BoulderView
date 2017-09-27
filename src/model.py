# from visuals import load,text_df
import numpy as np

from pymongo import MongoClient, errors
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import train_test_split
import pandas as pd


def load(filename):
    df = pd.read_csv(filename)
    df = df.drop_duplicates('Text').reset_index()
    df['Hashtags'] = df.Hashtags.apply(lambda x: x[1:-1].replace("'","").split(", "))
    df['Hashtags'] = df.Hashtags.apply(lambda x: [] if '#' not in x[0] else x)
    return df
df = load('../data/tweets.txt')
df_text = text_df(df)

df['Coordinates'] = df[['Longitude', 'Latitude']].apply(lambda x: tuple(x), axis=1)
df = df[df.Longitude.notnull()]
df = df[['Coordinates','Text']].reset_index(drop = True)

X = list(df.Text)
y = list(df.Coordinates)
d = {i:c for i,c in zip(range(len(X)),y)}


queries = ['it is a beautiful day','boulder is a nice town','i am not sure how i ended up in boulder']

vectorizer = TfidfVectorizer(stop_words='english')
vectors = vectorizer.fit_transform(X).toarray()
# words = vectorizer.get_feature_names()
tokenized_queries = vectorizer.transform(queries)
cosine_similarities = linear_kernel(tokenized_queries, vectors)
titles = y


def get_top_values(lst, n, labels):
    '''
    INPUT: LIST, INTEGER, LIST
    OUTPUT: LIST

    Given a list of values, find the indices with the highest n values.
    Return the labels for each of these indices.

    e.g.
    lst = [7, 3, 2, 4, 1]
    n = 2
    labels = ["cat", "dog", "mouse", "pig", "rabbit"]
    output: ["cat", "pig"]
    '''
    return [labels[i] for i in np.argsort(lst)[-1:-n-1:-1]][0]




# for i, query in enumerate(queries):
#     print(query)
#     print(get_top_values(cosine_similarities[i], 1, titles))
#     print("\n")

def final():
    return [(query,get_top_values(cosine_similarities[i], 1, titles)) for i,query in enumerate(queries)]
