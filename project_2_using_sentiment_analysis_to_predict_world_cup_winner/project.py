#!/usr/bin/env python3
'''
Project : Create a labeled world cup tweets dataset in csv file for each team
in order to predict the winner of the competition via sentiment analysis (using NLP)
'''

import tweepy
import numpy as np
import pandas as pd
from textblob import TextBlob # NLP

# Step 1 - Authenticate (Twitter API)

consumer_key = 'your key'
consumer_secret = 'your key'

access_token = 'your key'
access_token_secret = 'your key'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


# Step 2 - Create pandas dataframe with the values

teams = ['Argentina', 'Australia', 'Belgium', 'Brazil', 'Colombia', 'Costa Rica', 'Croatia', 'Denmark',
         'Egypt', 'England', 'France', 'Germany', 'Iceland', 'Iran', 'Japan', 'Korea Republic',
         'Mexico', 'Morocco', 'Nigeria', 'Panama', 'Peru', 'Poland', 'Portugal', 'Russia',
         'Saudi Arabia', 'Senegal', 'Serbia', 'Spain', 'Sweden', 'Switzerland', 'Tunisia', 'Uruguay']


def get_label(analysis, threshold = 0):
    '''
    Labelisation of tweets
    '''
    if analysis.sentiment.polarity > threshold:
        return 'Positive'
    else:
        return 'Negative'

all_polarities = dict() # Predict the winner

for team in teams:
    team_polarities = []
    # Create the DataFrame
    df = pd.DataFrame(columns ={'Tweet', 'Sentiment Polarity', 'Subjectivity', 'Label'})

    # Get the tweets about the teams
    team_tweets = api.search(q=[team, 'World Cup'], lang='en', count='50')
    # Append the features and labels
    for tweet in team_tweets:
        text = tweet.text
        # print(text)
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        team_polarities.append(polarity)
        subjectivity = analysis.sentiment.subjectivity
        label = get_label(analysis)
        df = df.append({'Tweet':text, 'Sentiment Polarity':polarity, 'Subjectivity':subjectivity, 'Label':label}, ignore_index=True) #append rows

    # Update all_polarities
    all_polarities[team] = np.mean(team_polarities)

    # Convert pandas dataframe to csv
    df.set_index('Tweet', inplace=True)
    df.to_csv('{}_tweets_analysed.csv'.format(team))

# printed the next winner, the one with the higher polarity

world_cup_winner = max(all_polarities, key=all_polarities.get)
winner_polarity = all_polarities[world_cup_winner]
print('The 2018 World Cup is {} with {} of polarity'.format(world_cup_winner, winner_polarity))
