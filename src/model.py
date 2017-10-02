# from dataframes import load
import numpy as np
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import pandas as pd

class TextModel(object):
    def __init__(self, filename,n):
        # self.filename = filename
        self.df, self.df_pics = self._initialize(filename)
        self.get_X_y()
        self.split()
        self.vectorize()
        self.predict(n)

    def _initialize(self,filename):
        df = pd.read_csv(filename)
        df = df.drop_duplicates('Text').reset_index()
        df['Hashtags'] = df.Hashtags.apply(lambda x: x[1:-1].replace("'","").split(", "))
        df['Hashtags'] = df.Hashtags.apply(lambda x: [] if '#' not in x[0] else x)
        df['Coordinates'] = df[['Longitude', 'Latitude']].apply(lambda x: tuple(x), axis=1)
        df_coords = df[df.Longitude.notnull()]
        df_coords = df_coords[(df_coords['Longitude']>=-105.380894)&(df_coords['Longitude']<=-105.107185)&(df_coords['Latitude']>=39.978093)&(df_coords['Latitude']<=40.095651)]
        df_coords = df_coords[['Coordinates','Text']].reset_index(drop = True)


        df_pics = df[df['Type']=='photo'].reset_index()
        df_pics = df_pics[["Text","Pic_Link","Coordinates"]]
        return df_coords,df_pics

    def get_X_y(self):
        X = list(self.df.Text)
        hashtags = [' #BoulderAthletes',' #boulderlife',' #BeBoulder',' #boulderco',' #boulder',' #bouldercolorado',' #Boulder',' Boulder']
        for word in hashtags:
            X = [x.lower().replace(word.lower(),'') for x in X]
        y = list(self.df.Coordinates)
        self.X, self.y =  X,y
        self.text = (self.df_pics.Text)
        self.link = (self.df_pics.Pic_Link)
        self.coords = (self.df_pics.Coordinates)

    def split(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.1, random_state = 13)


    def vectorize(self):
        vectorizer = TfidfVectorizer(stop_words='english')
        vectors = vectorizer.fit_transform(self.X_train).toarray()


        tokenized_queries = vectorizer.transform(self.text) # <------ X_test
        self.cosine_similarities = cosine_similarity(tokenized_queries, vectors)
        self.titles = self.y_train

    def predict(self,n):
        self.hold =  [[self.titles[k] for k in np.argsort(self.cosine_similarities[i])[:1:-1]] for i in range(len(self.text))] # <-- X_test
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
        return self.X_train, self.X_test, self.y_train, self.y_test, self.y_pred, self.truth, self.text,self.link,self.coords

    def acc(self):
        self.accuracy = sum(self.truth)/len(self.truth)
        return self.accuracy


if __name__ == '__main__':
    t = TextModel('../data/tweets.txt',3)

    # plot_accs = []
    # ind = list(range(1,6))
    # for r in range(1,31):
    #     print("------------------------------")
    #     print("TT_Split #{}:".format(r))
    #     accuracies = []
    #     for i in ind:
    #         tm = TextModel('../data/tweets.txt',i,r)
    #         tm.predict(i)
    #         X_train, X_test, y_train, y_test, y_pred, truth, text, link, coords = tm.variables()
    #         accuracies.append(tm.acc())
    #         # print("Accuracy with {} point(s): {}".format(i,tm.acc()))
    #     plot_accs.append(accuracies)
    #
    # avg_acc = [np.mean(i) for i in np.transpose(plot_accs)]
    # # for i in range(30):
    # #     plt.plot(ind,plot_accs[i],c='b')
    # plt.plot(ind,avg_acc,c = 'r')
    # plt.xlabel("Number of points")
    # plt.ylabel("Accuracy")
    # plt.title("Accuracy of model")
    # plt.show()
