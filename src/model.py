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
        df = load('../data/tweets.txt')
        df['Coordinates'] = df[['Longitude', 'Latitude']].apply(lambda x: tuple(x), axis=1)
        df = df[df.Longitude.notnull()]
        df = df[(df['Longitude']>=-105.380894)&(df['Longitude']<=-105.107185)&(df['Latitude']>=39.978093)&(df['Latitude']<=40.095651)]
        df = df[['Coordinates','Text']].reset_index(drop = True)
        self.df = df

    def get_X_y(self):
        X = list(self.df.Text)
        hashtags = ['#BoulderAthletes','#boulderlife','#BeBoulder','#boulderco','#boulder','#bouldercolorado','#Boulder','Boulder']
        for word in hashtags:
            X = [x.replace(word,'') for x in X]
        y = list(self.df.Coordinates)
        self.X, self.y =  X,y

    def split(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state = 13)


    def vectorize(self):
        vectorizer = TfidfVectorizer(stop_words='english')
        vectors = vectorizer.fit_transform(self.X_train).toarray()

        tokenized_queries = vectorizer.transform(self.X_test)
        self.cosine_similarities = linear_kernel(tokenized_queries, vectors)
        self.titles = self.y_train

    def predict(self,n):
        self.y_pred =  [[self.titles[k] for k in np.argsort(self.cosine_similarities[i])[-1:-n-1:-1]][:n] for i in range(len(self.X_test))]



    # def accuracies(self, N = 5):
    #     accuracies = []
    #     for t in range(1,6):
    #         y_pred = [[self.titles[k] for k in np.argsort(self.cosine_similarities[i])[-1:-t-1:-1]][:t] for i in range(len(self.X_test))]
    #         c = 0
    #         for i in range(len(self.y_test)):
    #             if self.y_test[i] in y_pred[i]:
    #                 c+=1
    #         acc = c/len(self.y_test)
    #         accuracies.append(acc)
    #         print("Accuracy for {} value(s): {}".format(t,acc))





#
# def rmse(y_pred,y):
#     r = [((y_pred[i][0]-y[i][0])**2 +(y_pred[i][0]-y[i][0])**2)**.5 for i in range(len(y))]
#     return np.sum(r)/len(r)
    # return r


if __name__ == '__main__':
    tm = TextModel()
    tm.get_X_y()
    tm.split()
    tm.vectorize()
    tm.predict(2)
