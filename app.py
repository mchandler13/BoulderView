from flask import Flask, render_template
from src.visuals import load,coordinates_df
# from src.model import final
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


df = load('data/tweets.txt')
df_coords = coordinates_df(df)


""" This is Bad"""

df['Coordinates'] = df[['Longitude', 'Latitude']].apply(lambda x: tuple(x), axis=1)
df = df[df.Longitude.notnull()]
df = df[(df['Longitude']>=-105.380894)&(df['Longitude']<=-105.107185)&(df['Latitude']>=39.978093)&(df['Latitude']<=40.095651)]
df = df[['Coordinates','Text']].reset_index(drop = True)

X = list(df.Text)
y = list(df.Coordinates)
d = {i:c for i,c in zip(range(len(X)),y)}

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# queries = ['it is a beautiful day','boulder is a nice town','i am not sure how i ended up in boulder']

vectorizer = TfidfVectorizer(stop_words='english')
vectors = vectorizer.fit_transform(X_train).toarray()

tokenized_queries = vectorizer.transform(X_train)
cosine_similarities = linear_kernel(tokenized_queries, vectors)
titles = y_train


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
    return [labels[i] for i in np.argsort(lst)[-1:-n-1:-1]]




# for i, query in enumerate(queries):
#     print(query)
#     print(get_top_values(cosine_similarities[i], 1, titles))
#     print("\n")

def final():
    return [get_top_values(cosine_similarities[i], 4, titles) for i in range(len(X_test))]

y_pred = final()




result =  [y_pred[i]==y_test[i] for i in range(len(y_pred))]

def rmse(y_pred,y):
    r = [((y_pred[i][0]-y[i][0])**2 +(y_pred[i][0]-y[i][0])**2)**.5 for i in range(len(y))]
    return np.sum(r)/len(r)
    # return r


accuracy = np.sum(result)/len(result)


""" ------------------- """




# initialize the Flask app, note that all routing blocks use @app
app = Flask(__name__)  # instantiate a flask app object

# routing blocks - note there is only one in this case - @app.route('/')

# home page - the first place your app will go
@app.route('/', methods = ['GET', 'POST'])  # GET is the default, more about GET and POST below
# the function below will be executed at the host and port followed by '/'
# the name of the function that will be executed at '/'. Its name is arbitrary.
def index():
    d = [list(df_coords["Longitude"]),list(df_coords["Latitude"]),list(df_coords["Num_Hashtags"])]
    return render_template('home.html',data = d)

@app.route('/predict',methods = ['GET','POST'])
def predict():
    i = np.random.randint(len(y_pred))
    # e = ((y_pred[i][0]-y_test[i][0])**2 +(y_pred[i][0]-y_test[i][0])**2)**.5
    return render_template("predict.html",data = [X_test[i],y_pred[i],y_test[i]])
# no more routing blocks

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    # the combination of host and port are where we look for it in our browser
    # e.g. http://0.0.0.0:8080/
    # setting debug=True to see error messages - wouldn't do this on a final deployed app
