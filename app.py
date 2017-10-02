from flask import Flask, render_template
from src.dataframes import load,coordinates_df
from src.model import TextModel
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
import folium

df = load('data/tweets.txt')
df_coords = coordinates_df(df)

N = 3
tm = TextModel('data/tweets.txt',N)
X_train, X_test, y_train, y_test, y_pred, truth, text, link, coords = tm.variables()
# accuracy = tm.acc()


""" BAD"""






""" -------------------"""


app = Flask(__name__)

""" Home Page """
@app.route('/',methods = ['GET','POST'])
def index():
    # d = [list(df_coords["Longitude"]),list(df_coords["Latitude"]),list(df_coords["Num_Hashtags"])]
    return render_template('home.html')



""" Predict Page """
@app.route('/predict',methods = ['GET','POST'])
def predict():
    i = np.random.randint(len(text))
    # e = ((y_pred[i][0]-y_test[i][0])**2 +(y_pred[i][0]-y_test[i][0])**2)**.5
    # data = [X_test[i],y_pred[i],y_test[i],truth[i],accuracy]
    data = [text[i],y_pred[i],coords[i],link[i],text[i]]

    return render_template("predict.html",data = data)




""" Plot page """
@app.route('/plots', methods = ['GET', 'POST'])
def plots():
    d = [list(df_coords["Longitude"]),list(df_coords["Latitude"]),list(df_coords["Num_Hashtags"])]
    return render_template('plots.html',data = d)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    # the combination of host and port are where we look for it in our browser
    # e.g. http://0.0.0.0:8080/
    # setting debug=True to see error messages - wouldn't do this on a final deployed app
