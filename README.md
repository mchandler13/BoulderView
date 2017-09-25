# BoulderView
Using Twitter to predict where photos are being taken, based on the text associated with the picture. MORE HERE

## Table of Contents
1. [Early Steps](#Early-Steps) <-- Figure out this issue
   * [Gathering Data](#Gathering-The-Data)
   * [Building The Dataset](#Building-the-Dataset)
   * [EDA](#EDA)


## Early Steps
I decided on Twitter, due to the simlicity of it's API. After gaining access, it was very easy to get the relevant information.
### Gathering Data
Pulling Data every hour, and loading it into a .txt file, gaining roughly 1000 lines at each pull. Much of this data would be missing information, such as latitude/longitude.
### Building The Dataset
After each pull, new data would be added into the dataframe, with any repeats being omitted. The fetures I'm using are as follows:
* **ID**: The Tweet ID
* **Type**: Picture, Video, Animated Gif, Other
* **Pic_link**: the link to the picture, if applicable
* **Longitude**: The longitude of the tweet
* **Latitude**: The latitude of the tweet
* **Text**: The text associated with the tweet
* **Hashtags**: The hashtags associated with the tweet
* **Created_At**: The date/time when the tweet was posted
* **Coordinates**: the longitude/latitude coordinates of the tweet

## EDA
Dropping all rows where coordinates were NaN, and then grouping the dataframe by coordinates, and getting the count of each feature. Then plotting the results over a map of Boulder, with the size of each marker indicating the number of tweets sent from each location. This created a new dataframe called df_coords, containing the counts of the Type column ("Photo or "Not Photo"). 
<img alt="EDA_1" src="data/images/EDA_2.jpg" width='700' height = '450'>
Made with [Seaborn](https://seaborn.pydata.org/)



Moving forward, I knew I'd be using interactive plots, so I looked into a few:
* [Bokeh](https://bokeh.pydata.org/en/latest/) EXPLANATIONS OF THIS
* [Plotly](https://plot.ly/) EXPLANATIONS OF THIS 
* [Folium](https://folium.readthedocs.io/en/latest/) EXPLANATIONS OF THIS

Decided to use Plotly, due to it's ease of use, and ability to interact with webapps. [Here](https://plot.ly/~martychandler13/8.embed) is an early example using Plotly. It's simple to use, and has built-in hover properties. BOULDER MAP IS NOT APPEARING UNDER SCATTER PLOT, FIX THIS.

AsDict() picture of this
