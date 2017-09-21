import numpy as np
import pandas as pd
from collections import Counter
import os
import plotly.plotly as py
import plotly
from plotly.graph_objs import *
from nltk.tokenize import TweetTokenizer


# d = {'id':[1,1,2],'text':['the dog ran far','my dog is my best friend','Cats are cool']}
# df = pd.DataFrame(d)
# df['coordinates'] = df[['longitude', 'latitude']].apply(lambda x: tuple(x), axis=1)
# df_coords = df[df.longitude.notnull()]
# df_dum = pd.get_dummies(df_coords['type'])
# df_coords = pd.concat([df_coords,df_dum],axis = 1)
# df_coords.drop('type',axis = 1,inplace = True)
# df['text'] = df['text'].apply(lambda x: x.split(" "))
# df = df.groupby('coordinates').agg({'text':sum}).reset_index()
# df['text'] = df['text'].apply(lambda x: Counter(x).most_common(4))

tt  = TweetTokenizer(strip_handles=True, reduce_len=True, preserve_case=False)
tt.tokenize('best day ever #Boulder OMG')
