# BoulderView
In coordination with the City Of Boulder, I will be using Twitter to predict where photos are being taken, based on the text associated with the picture. 

## Table of Contents
1. [Data](#data)
   * [Tweets](#tweets)
   * [Gathering Data](#gathering-data)
   * [Building The Dataset](#building-the-dataset)
   * [EDA](#eda)
2. [NLP](#nlp)
3. [The Model](#the-model)
   * [First Model](#first-model)
   * [Accuracy](#accuracy)
4. [Web Application](#web-application)


## Data
Originally, I was going to be using a database from the City Of Boulder, but none of the files contained Geocode information. I investigated the APIs of Facebook, Twitter, and Instagram. Facebook wasn't allowing access at the time, and I still haven't heard back from Instagram, but Twitter has been extremely helpful. The API is very easy to use, and provides a wealth of information.

### Tweets
Most people would say that a Tweet is simply anything posted on Twitter (usually text or a picture). In reality, a Tweet contains a great deal of information, ranging from geographic information to the time of the tweet. This type data provides information about other data. We call this **metadata**, and it can be extremely useful.

### Gathering Data
I made a data pull every hour, and loaded it into a .txt file, gaining roughly 1000 lines at each pull. Much of this data would be missing information, such as latitude/longitude. Also, many of the rows would be repeats, so I will need to drop them upon reading them into my database. Due to the limited amount of time, my dataset will be relatively small.


### Building The Dataset
After each pull, new data would be added into the dataframe, with any repeats being omitted. The features I'll be using are as follows:
* **ID**: The Tweet ID
* **Type**: Picture, Video, Animated Gif, Other
* **Pic_link**: the link to the picture, if applicable
* **Longitude**: The longitude of the tweet
* **Latitude**: The latitude of the tweet
* **Text**: The text associated with the tweet
* **Hashtags**: The hashtags associated with the tweet
* **Created_At**: The date/time when the tweet was posted
* **Coordinates**: the longitude/latitude coordinates of the tweet
<img alt="AsDict" src="data/images/AsDict.jpg" width='500' height = '400'>
<sub>**Figure 1:** A single Tweet in the form of a dictionary, which allows me to gather metadata with ease</sub>

## EDA
Dropping all rows where coordinates were NaN, and then grouping the dataframe by coordinates, and getting the count of each feature. Then plotting the results over a map of Boulder, with the size of each marker indicating the number of tweets sent from each location. This created a new dataframe called df_coords, containing the counts of the Type column ("Photo or "Not Photo"). 
<img alt="EDA_1" src="data/images/EDA_2.jpg" width='700' height = '450'>
<sub>Made with [Seaborn](https://seaborn.pydata.org/)</sub>



Moving forward, I knew I'd be using interactive plots, so I looked into a few:
* [Bokeh](https://bokeh.pydata.org/en/latest/) Useful for Visualization of large datasets
* [Plotly](https://plot.ly/) Creates dashboards for web applicastions
* [Folium](https://folium.readthedocs.io/en/latest/) Useful for mapping data

Initially, I decided to use Plotly, due to it's ease of use, and ability to interact with webapps. [Here](https://plot.ly/~martychandler13/8.embed) is an early example using Plotly. It's simple to use, and has built-in hover properties. Later, I switched to Folium, because it allows for interactive maps.


# NLP
NLP stands for Natural Language Processing. It is a field of Computer Science that allows computers to make sense of everyday (human) language. MAYBE ADD A FEW LINKS TO EXAMPLES HERE. I will be using NLP, because every Tweet has text associated with it, and I will be able to make predictions regarding a new Tweet based on the text of existing tweets.

# The Model

## First Model
I split the data into a training set and a testing set. Using tfidfVectorizer I created a Matrix of [cosine similarities](https://en.wikipedia.org/wiki/Cosine_similarity). The process of testing the model is as follows:

1) Pull a Tweet from the testing dataset
2) Compute the cosine similarity between the text of that tweet, and the text of all the tweets from the the training dataset.
3) Return the coordinates of the tweet (from the training dataset) that has the highest cosine similarity with the test tweet.
4) Compare the predicted coordinates to the actual coordinates.
5) Repeat 1-4 until a prediction has been made for each Tweet from the testing dataset.
6) Compute the accuracy by dividing the number of correct predictions by the total number of predictions made.

## Accuracy
The average accuracy for my model was around .648, meaning roughly 65% of the time, my model would be able to accurately predict the location of a picture based on its text. The low accuracy is largely due to the small size of my dataset. As time goes on, and I will be able to collect more Tweets, and the accuracy will increase. I also knew that limiting my score by only considering a prediction to be successfull if the actual coordinates equaled the predicted coordinates. I investigated what happened when I defined a success by the actual coordinates being in the top N predictions, instead of just the top prediction:

<img alt="accuracy_plot" src="data/images/avg_acc_plot.png" width='500' height = '350'>
<img alt="accuracy_table" src="data/images/Accuracy_table.png" width='300' height = '180'>

I made the decision for my model to check the top 3 values and return those coordinates, becuase it resulted in a 10% increase in accuracy. Here is an example:

Once the model was running, I could pull a random Tweet (picture) and predict it's location based on the associated text.
Low accuracy, but haven't made any adjustments to it yet, and the dataset is still pretty small. Also, I'm only using the text of the tweet 

# Web Application

[Home](https://raw.githubusercontent.com/mchandler13/BoulderView/master/data/images/Boulder_home.png) page displays a map of Boulder with Hover effects

[Predict](https://github.com/mchandler13/BoulderView/blob/master/data/images/Boulder_predict1.png) page makes a prediction as to the location of the tweet. Ultimately, there will be a map that shows the predicted point and the actual point (if present), and the error associated

**Interesting issue** converting longitude/latitude to miles is a challenge




