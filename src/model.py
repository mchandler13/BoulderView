from visuals import load,coordinates_df
import numpy as np
df = load('../data/tweets.txt')
df_coords = coordinates_df(df)
df_coords.head()
print(df_coords.columns)
