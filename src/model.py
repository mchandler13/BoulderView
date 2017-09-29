# from dataframes import load
import numpy as np

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

class TextModel(object):
    def __init__(self, filename):
        # self.filename = filename
        self.df = self._initialize(filename)

    def _initialize(self,filename):
        df = pd.read_csv(filename)
        df = df.drop_duplicates('Text').reset_index()
        df['Hashtags'] = df.Hashtags.apply(lambda x: x[1:-1].replace("'","").split(", "))
        df['Hashtags'] = df.Hashtags.apply(lambda x: [] if '#' not in x[0] else x)
        df['Coordinates'] = df[['Longitude', 'Latitude']].apply(lambda x: tuple(x), axis=1)
        df = df[df.Longitude.notnull()]
        df = df[(df['Longitude']>=-105.380894)&(df['Longitude']<=-105.107185)&(df['Latitude']>=39.978093)&(df['Latitude']<=40.095651)]
        df = df[['Coordinates','Text']].reset_index(drop = True)
        return df

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
        self.hold =  [[self.titles[k] for k in np.argsort(self.cosine_similarities[i])[:1:-1]] for i in range(len(self.X_test))]
        self.y_pred = []
        for i in self.hold:
            temp = []
            for j in i:
                if j not in temp:
                    temp.append(j)
            self.y_pred.append(temp)
        self.y_pred = [x[:n] for x in self.y_pred]

    def variables(self):
        self.truth = [self.y_test[i] in self.y_pred[i] for i in range(len(self.y_test))]
        return self.X_train, self.X_test, self.y_train, self.y_test, self.y_pred, self.truth
