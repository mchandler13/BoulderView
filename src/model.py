from dataframes import load,text_df
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
import matplotlib.pyplot as plt

class TextModel(object):
    def __init__(self):

def dataframe():
    df = load('../data/tweets.txt')
    df['Coordinates'] = df[['Longitude', 'Latitude']].apply(lambda x: tuple(x), axis=1)
    df = df[df.Longitude.notnull()]
    df = df[(df['Longitude']>=-105.380894)&(df['Longitude']<=-105.107185)&(df['Latitude']>=39.978093)&(df['Latitude']<=40.095651)]
    df = df[['Coordinates','Text']].reset_index(drop = True)
    return df


def get_X_y(df):
    X = list(df.Text)
    hashtags = ['#BoulderAthletes','#boulderlife','#BeBoulder','#boulderco','#boulder','#bouldercolorado','#Boulder','Boulder']
    for word in hashtags:
        X = [x.replace(word,'') for x in X]
    y = list(df.Coordinates)
    return X,y


def vectorize(X_train,X_test,y_train):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(X_train).toarray()

    tokenized_queries = vectorizer.transform(X_test)
    cosine_similarities = linear_kernel(tokenized_queries, vectors)
    titles = y_train
    return cosine_similarities, titles


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
    z = list(zip(lst,labels))
    z =list(set(z))
    lst,labels = list(zip(*z))
    lst = list(lst)
    labels = list(labels)
    return [labels[i] for i in np.argsort(lst)[-1:-n-1:-1]][:n]

def final(n,X_test):
    return [get_top_values(cosine_similarities[i], n, titles) for i in range(len(X_test))]


def accuracies(X_test,y_test,N = 5):
    accuracies = []
    for k in range(1,N+1):
        y_pred = final(k,X_test)
        c = 0
        for i in range(len(y_test)):
            if y_test[i] in y_pred[i]:
                c+=1
        acc = c/len(y_test)
        accuracies.append(acc)
        print("Accuracy for {} value(s): {}".format(k,acc))

def plot():
    plt.scatter(list(range(1,50)),accuracies)
    plt.xlabel("Number of Values")
    plt.ylabel("Accuracy")
    plt.title("Initial Model")
    plt.show()





def rmse(y_pred,y):
    r = [((y_pred[i][0]-y[i][0])**2 +(y_pred[i][0]-y[i][0])**2)**.5 for i in range(len(y))]
    return np.sum(r)/len(r)
    # return r


if __name__ == '__main__':
    df = dataframe()
    X,y = get_X_y(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 13)
    cosine_similarities,titles = vectorize(X_train,X_test,y_train)
    y_pred = [get_top_values(cosine_similarities[i], 1, titles) for i in range(len(X_test))]


    result =  [y_pred[i]==y_test[i] for i in range(len(y_pred))]

    accuracy = np.sum(result)/len(result)
    accuracies(X_test,y_test,5)
