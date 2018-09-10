#!/usr/bin/env python3
'''
Project :
- Create a method to fetch and parse a music recommendation dataset
- Use 3 different models for recommendation, compare their results,
and then only print the recommendations for the best one.
'''

import numpy as np
import pandas as pd
from scipy import sparse
# Allows us to perform recommendation algorithms
from lightfm import LightFM

# Step 1 - Fetch and parse a recommendation dataset

def fetch_dataset(num_rows=1000000):
    '''
    Preprocessing the dataset
    Returning a sparse matrix in coo format
    '''
    # Create a dataframe from LastFM dataset, Parsing a tsv file
    df = pd.read_csv('lastfm_dataset.tsv',
                     sep='\t',
                     nrows=num_rows,
                     names=['User', 'Artist_Id', 'Artist_Name', 'Total-Plays'])

    # Visualize our dataframe
    # print(df.head())
    # print(df.tail())

    # Converting our dataframe into sparse matrix

    values = df.values # numpy.ndarray

    # Data to create our coo_matrix
    data, row, col = [], [], []

    # Artists by id, and users
    artists, users = {}, {}

    for line in values:
        user = line[0]
        artist_id = line[1]
        artist_name = line[2]
        plays = int(line[3])

        # Add user in the dictionary
        if user not in users:
            users[user] = len(users)

        # Add artist in the dictionary
        if artist_id not in artists:
            artists[artist_id] = {'name' : artist_name, 'id': len(artists)}

        # We add the artist in the data if the artist was played > 50 times
        if plays > 100:
            data.append(plays)
            row.append(users[user])
            col.append(artists[artist_id]['id'])

    coo_sparse_matrix = sparse.coo_matrix((data, (row,col)))

    full_data = {'coo_matrix' : coo_sparse_matrix,
                 'artists' : artists,
                 'users' : len(users)}

    return full_data


# Step 2 - Create three diffrent model

full_data = fetch_dataset()

def get_recommendations(users_ids):

    results = dict()

    losses = ['warp', 'bpr', 'warp-kos']

    n_items = full_data['coo_matrix'].shape[1]

    for loss in losses:
        # Create model
        model = LightFM(loss=loss)

        # Train model
        # The dataset is given 'epoch' time to the algorithm
        # Numb_threads : parallel computation, not be higher than the number of physical core
        model.fit(full_data['coo_matrix'], epochs=10, num_threads=2)

        print('********* With {} algorithm *********\n'.format(loss))
        for user in users_ids:

            scores = model.predict(user, np.arange(n_items))
            top_scores = np.argsort(-scores)[:3]

            print('Recommendations for user {}:'.format(user))

            for x in top_scores.tolist():
                for artist, dict_artist in full_data['artists'].items():
                    if int(x) == dict_artist['id']:
                        print('   - {}'.format(dict_artist['name']))

            print('\n') # Get it pretty


user_1 = input('Select user_1 (0 to {}): '.format(full_data['users']))
user_2 = input('Select user_2 (0 to {}): '.format(full_data['users']))
user_3 = input('Select user_3 (0 to {}): '.format(full_data['users']))
print('\n') # Get it pretty

get_recommendations([user_1, user_2, user_3])
