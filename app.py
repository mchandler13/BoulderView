from flask import Flask, render_template
from src.visuals import load,coordinates_df
import numpy as np
df = load('data/tweets.txt')
df_coords = coordinates_df(df)


# initialize the Flask app, note that all routing blocks use @app
app = Flask(__name__)  # instantiate a flask app object

# routing blocks - note there is only one in this case - @app.route('/')

# home page - the first place your app will go
@app.route('/', methods = ['GET', 'POST'])  # GET is the default, more about GET and POST below
# the function below will be executed at the host and port followed by '/'
# the name of the function that will be executed at '/'. Its name is arbitrary.
def index():
    d = [list(df_coords["Longitude"]),list(df_coords["Latitude"]),list(df_coords["Num_Hashtags"])]
    # d = [list(df_coords["Longitude"]),list(df_coords["Latitude"]),df_coords[["Num_Hashtags","photo","Not_Specified"]]]
    return render_template('home.html',data = d)

@app.route('/predict',methods = ['GET','POST'])
def predict():
    i = np.random.randint(df_coords.Hashtags.shape[0])
    h = df_coords.Hashtags[i]
    c = df_coords.Coordinates[i]
    l = len(h)
    return  render_template("predict.html",data = [i,h,c,l])
# no more routing blocks

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    # the combination of host and port are where we look for it in our browser
    # e.g. http://0.0.0.0:8080/
    # setting debug=True to see error messages - wouldn't do this on a final deployed app
