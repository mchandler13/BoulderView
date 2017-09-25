import twitter
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.misc import imread
import numpy as np

def access_api():
    """ Access the Twitter API """
    twitter_consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    twitter_consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    twitter_access_token = os.environ['TWITTER_ACCESS_TOKEN']
    twitter_access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
    return twitter.Api(consumer_key=twitter_consumer_key,
                      consumer_secret=twitter_consumer_secret,
                      access_token_key=twitter_access_token,
                      access_token_secret=twitter_access_token_secret)

def get_results(api):
    hashtags = ['#BoulderAthletes','#boulderlife','#Buffs','#BeBoulder','#FolsomField','#bouldercouncil','#CUBoulder','#boulderco','#boulder','#bouldercolorado','@bouldercolorado','@downtownboulder','@BoulderCountyOS','#chautauqua','#flatirons','#flatironsboulder','#beboulder','#pearlstreet']
    results = []
    for hashtag in hashtags:
        results += api.GetSearch(term = hashtag,count = 120)
    results += api.GetSearch(geocode = [40.0267216,-105.3030757,"2mi"],count = 100)
    return results


def create_df(results):
    med = []
    lat = []
    lon = []
    ids = []
    text = []
    tweet_type = []
    date = []
    hashtags = []
    for r in results:
        text.append(r.text)
        d = r.AsDict()
        ids.append(d['id'])
        date.append(d['created_at'])
        if 'media' not in list(d.keys()):
            med.append("")
            tweet_type.append("Not_Specified")
        else:
            med.append(str(d['media'][0]['media_url_https']))
            tweet_type.append(d['media'][0]['type'])
        if 'geo' not in list(d.keys()):
            lat.append("")
            lon.append("")
        else:
            lat.append(d['geo']['coordinates'][0])
            lon.append(d['geo']['coordinates'][1])
        # if 'hashtag' not in list(d.keys()):
        #     hashtags.append([])
        # else:
        h = d['hashtags']
        htag = ['#'+i['text'] for i in h]
        hashtags.append(htag)

    d = {'ID':ids,'Type':tweet_type,'Latitude':lat,'Longitude':lon,'Pic_Link':med,'Text':text,'Hashtags':hashtags,'Created_At':date}
    df = pd.DataFrame(d)
    df.fillna(0,inplace = True)

    df = df[['ID','Type','Pic_Link','Longitude','Latitude','Text','Hashtags','Created_At']]
    return df

def write_to_file(df,filename):
    if os.stat(filename).st_size == 0:
        header = True
    else:
        header = False
    df.to_csv(filename, index=None,header = header, sep=',', mode='a')

if __name__ == '__main__':
    api = access_api()
    results = get_results(api)
    df = create_df(results)
    write_to_file(df,'../data/tweets.txt')
