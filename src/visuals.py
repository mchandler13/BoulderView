import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.misc import imread
import numpy as np
from collections import Counter
import plotly.plotly as py
import plotly
from plotly.graph_objs import *


def load(filename):
    df = pd.read_csv(filename)
    df = df.drop_duplicates('Text').reset_index()
    df['Hashtags'] = df.Hashtags.apply(lambda x: x[1:-1].replace("'","").split(", "))
    df['Hashtags'] = df.Hashtags.apply(lambda x: [] if '#' not in x[0] else x)
    return df

def pictures_df(dataframe):
    df = dataframe
    df = df[df['Type']=='photo']
    return df

def hashtag_df(dataframe):
    df = dataframe
    # df['Coordinates'] = df[['Longitude', 'Latitude']].apply(lambda x: tuple(x), axis=1)
    df = df[df.Longitude.notnull()]
    df = df.groupby(['Longitude','Latitude']).agg({'Hashtags':sum}).reset_index()
    df['Hashtags'] = df['Hashtags'].apply(lambda x: Counter(x).most_common(3))
    return df

def text_df(dataframe):
    df = dataframe
    df['Coordinates'] = df[['Longitude', 'Latitude']].apply(lambda x: tuple(x), axis=1)
    df = df[df.Longitude.notnull()]
    df_dum = pd.get_dummies(df['Type'])
    df = pd.concat([df,df_dum],axis = 1)
    df.drop('Type',axis = 1,inplace = True)
    df['Text'] = df['Text'].apply(lambda x: x.split(" "))
    df = df.groupby('Coordinates').agg({'Text':sum}).reset_index()
    df['Text'] = df['Text'].apply(lambda x: Counter(x).most_common(1)[0])
    return df


def coordinates_df(dataframe):
    df = dataframe
    df['Coordinates'] = df[['Longitude', 'Latitude']].apply(lambda x: tuple(x), axis=1)
    df_coords = df[df.Longitude.notnull()]
    df_dum = pd.get_dummies(df_coords['Type'])
    df_coords = pd.concat([df_coords,df_dum],axis = 1)
    df_coords.drop('Type',axis = 1,inplace = True)
    df_coords = df_coords.groupby('Coordinates').agg({'photo':sum,'Not_Specified':sum,'Hashtags':sum}).reset_index('Coordinates')
    df_coords = df_coords[['Coordinates','photo','Not_Specified','Hashtags']]
    df_coords['Count'] = df_coords['photo']+df_coords['Not_Specified']
    df_coords['Longitude'] = df_coords.Coordinates.apply(lambda x: x[0])
    df_coords['Latitude'] = df_coords.Coordinates.apply(lambda x: x[1])
    df_coords = df_coords[(df_coords['Longitude']>=-105.380894)&(df_coords['Longitude']<=-105.107185)&(df_coords['Latitude']>=39.978093)&(df_coords['Latitude']<=40.095651)]
    return df_coords

def plot_first(dataframe):
    df_coords = dataframe
    m_lat = df_coords["Latitude"].median()
    m_lon = df_coords["Longitude"].median()
    img = imread("/Users/Marty/Desktop/Boulder.png")
    size = [10*i for i in list(df_coords['Count'])]
    alpha = [i/26 for i in list(df_coords['Count'])]
    current_palette = sns.color_palette("Set2", 10)
    sns.lmplot(x = 'Longitude',y = 'Latitude',data = df_coords, hue = 'photo',fit_reg = False,scatter_kws = {'alpha':.6,'s':size})
    plt.scatter([m_lon],[m_lat],s=40,c = '#FF2266')
    plt.title("Map of Boulder: {} points, {} Tweets".format(df_coords.shape[0],df_coords['Count'].sum()),fontsize = 20)
    plt.xlabel("Longitude",fontsize = 10)
    plt.ylabel("Latitude",fontsize = 10)
    plt.imshow(img,extent = [-105.380894,-105.107185,39.978093,40.095651])
    plt.show()
def plotly_plot(dataframe):
    df_coords = dataframe
    trace0 = Scatter(
        x=list(df_coords['Longitude']),
        y=list(df_coords['Latitude']),
        # x = [1,2,3,4,5],
        # y = [3,2,1,4,5],
        mode = 'markers'
    )
    layout = Layout(
        images = [dict(source = "https://raw.githubusercontent.com/mchandler13/BoulderView/master/Boulder.png",
                  xref= "x",
                  yref= "y",
                  x= -105.4,
                  y= 40.08,
                  sizex= .3,
                  sizey= .1,
                  sizing= "stretch",
                  opacity= 0.7,
                  layer= "below")],
        xaxis=dict(range = [-105.4,-105.1]),
        yaxis=dict(range = [39.98,40.08])
    )

    data = Data([trace0])
    fig = Figure(data=data, layout = layout)
    plot_url = py.plot(fig, filename='first_geo')




if __name__ == '__main__':
    df = load('../data/tweets.txt')
    df_coords = coordinates_df(df)
    dfc = df_coords[df_coords['Count']>=2].reset_index()
    # plot_first(df_coords)
    # plotly_plot(df_coords)
    df_hashtags = hashtag_df(df)
    df_pics = pictures_df(df)
    df_text = text_df(df)


    df_coords['text'] =df_coords['Count'].astype(str)

    # data = [ dict(
    #         type = 'bar',
    #         showlegend = True,
    #         x = df_coords['Coordinates'],
    #         y = df_coords['Count'],
    #         mode = 'markers',
    #         marker = dict(
    #             size = 8,
    #             opacity = 0.4,
    #             reversescale = True,
    #             autocolorscale = False,
    #             symbol = 'circle',
    #             line = dict(
    #                 width=1,
    #                 color='rgba(102, 102, 102)')))]
    #
    # layout = dict(
    #         title = 'Boulder Tweets',
    #         hovermode='closest',
    #         images = [dict(source = "https://raw.githubusercontent.com/mchandler13/BoulderView/master/data/images/Boulder.jpg",
    #                   xref= "x",
    #                   yref= "y",
    #                   x= -105.4,
    #                   y= 40.08,
    #                   sizex= .3,
    #                   sizey= .1,
    #                   sizing= "stretch",
    #                   opacity= 0.7,
    #                   layer= "below")]
    #     )
    #
    # fig = dict( data=data, layout=layout )
    # py.plot(fig, validate=False, filename='thingy' )


    import plotly.plotly as py
    import plotly.graph_objs as go

    data = [
        go.Scatter(
            x=[0,1,2],
            y=[4,6,4],
            name='Number of Tweets per lcation',
            marker=Marker(
                color='#2ca02c'
            )
        )
    ]

    layout = go.Layout(
        title="Number of songs listed in the Guardian's<br><em>Top 1,000 Songs to Hear Before You Die</em> per artist with 4 or more songs",
        font=dict(
            family='Georgia, serif',
            color='#635F5D'
        ),
        plot_bgcolor='#EFECEA'
    )
    fig = go.Figure(data=data, layout=layout)
    plot_url = py.plot(fig)













x = 5
