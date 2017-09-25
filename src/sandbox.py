import numpy as np
import pandas as pd
from collections import Counter
import os
import plotly.plotly as py
import plotly
from plotly.graph_objs import *
from nltk.tokenize import TweetTokenizer


d = {'id':[1,1,2],'text':["['#Boulder', '#CO']","['#DogPark']","['#icecream']"]}
df = pd.DataFrame(d)
# df['coordinates'] = df[['longitude', 'latitude']].apply(lambda x: tuple(x), axis=1)
# df_coords = df[df.longitude.notnull()]
# df_dum = pd.get_dummies(df_coords['type'])
# df_coords = pd.concat([df_coords,df_dum],axis = 1)
# df_coords.drop('type',axis = 1,inplace = True)
# df['Text'] = df['Text'].apply(lambda x: x.split(" "))
# df = df.groupby('Coordinates').agg({'Text':sum}).reset_index()
# df['Text'] = df['Text'].apply(lambda x: Counter(x).most_common(4))









tt  = TweetTokenizer(strip_handles=True, reduce_len=True, preserve_case=False)
tt.tokenize('best day ever #Boulder OMG')

# df_coords['text'] =df_coords['Hashtags'].astype(str)
#
# scl = [ [0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
#     [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"] ]
#
# data = [ dict(
#         type = 'scatter',
#         x = df_coords['Longitude'],
#         y = df_coords['Latitude'],
#         text = df_coords['text'],
#         mode = 'markers',
#         marker = dict(
#             size = 8,
#             opacity = 0.4,
#             reversescale = True,
#             autocolorscale = False,
#             symbol = 'circle',
#             line = dict(
#                 width=1,
#                 color='rgba(102, 102, 102)'
#             ),
#             colorscale = scl,
#             cmin = 0,
#             colorbar=dict(
#                 title="Incoming flightsFebruary 2011"
#             )
#         ))]
#
# layout = dict(
#         title = 'Most trafficked US airports<br>(Hover for airport names)',
#         colorbar = True,
#         geo = dict(
#             scope='usa',
#             projection=dict( type='albers usa' ),
#             showland = True,
#             landcolor = "rgb(250, 250, 250)",
#             subunitcolor = "rgb(217, 217, 217)",
#             countrycolor = "rgb(217, 217, 217)",
#             countrywidth = 0.5,
#             subunitwidth = 0.5
#         ),
#     )
#
# fig = dict( data=data, layout=layout )
# py.plot(fig, validate=False, filename='d3-airports' )
