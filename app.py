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


df = load('data/tweets.txt')
df_coords = coordinates_df(df)
N = 3
tm = TextModel('data/tweets.txt')
tm.get_X_y()
tm.split()
tm.vectorize()
tm.predict(N)
X_train, X_test, y_train, y_test, y_pred, truth = tm.variables()

""" BAD"""
import folium
# # location=[40.036872, -105.2440395]
# map_osm = folium.Map(location=[40, -105.25],tiles = 'Stamen Terrain',zoom_start = 13)
# lat = df_coords.Latitude
# lon = df_coords.Longitude
# c = df_coords.Count
# for i in range(len(lon)):
#     folium.Marker([lat[i],lon[i]],icon=folium.Icon(color='#FF0000'),popup=str(c[i])).add_to(map_osm)
# map_osm.save('/Users/Marty/Desktop/map.html')





""" -------------------"""




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

    i = np.random.randint(len(tm.y_pred))

    map_osm = folium.Map(location=[40, -105.25],tiles = 'Stamen Terrain',zoom_start = 13)
    lon, lat = zip(*y_pred[i])
    for k in range(len(lon)):
        folium.Marker([lat[k],lon[k]],icon=folium.Icon(color='red'),popup='Timberline Lodge').add_to(map_osm)
    # folium.Marker(,icon=folium.Icon(color='blue'),popup='Actual Location').add_to(map_osm)
    folium.CircleMarker([y_test[i][1],y_test[i][0]],
                    radius=20,
                    popup='Actual Location',
                    color='#3186cc',
                    fill_color='#3186cc',
                   ).add_to(map_osm)
    map_osm.save('templates/map.html')
    # e = ((y_pred[i][0]-y_test[i][0])**2 +(y_pred[i][0]-y_test[i][0])**2)**.5
    return render_template("predict.html",data = [X_test[i],y_pred[i],y_test[i],truth[i]])
# no more routing blocks

@app.route('/map', methods = ['GET', 'POST'])  # GET is the default, more about GET and POST below
# the function below will be executed at the host and port followed by '/'
# the name of the function that will be executed at '/'. Its name is arbitrary.
def map():
    return render_template('map.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    # the combination of host and port are where we look for it in our browser
    # e.g. http://0.0.0.0:8080/
    # setting debug=True to see error messages - wouldn't do this on a final deployed app
