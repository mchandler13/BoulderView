# BoulderView
Using social networks to predict where photos are being taken, based on the associated text. 

## Table of Contents
1. [Early Steps](#Early-Steps)
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

### EDA
Dropping all rows where coordinates were NaN, and then grouping the dataframe by coordinates, and getting the count of each feature. Then plotting the results over a map of Boulder, with the size of each marker indicating the number of tweets sent from each location.

<img alt="EDA_1" src="data/images/EDA_1.jpg" width='800' height = '550'>
