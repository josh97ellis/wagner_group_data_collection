"""
Contains function that defines the data
to extract from the reddit api call
"""
import pandas as pd
from datetime import datetime


def response_table(res):
    """
    Table structure for reddit api resonse
    Fields:
        {name, created_utc, author, subreddit,
        title, selftext, url, media}
    """
    # initialize dataframe for pulling data in loop
    df = pd.DataFrame()

    # Get data from response
    for post in res.json()['data']['children']:
        post_df = pd.DataFrame({
            'name': post['data']['name'],
            'created_utc': (
                datetime.utcfromtimestamp(
                    post['data']['created_utc'])
            ),
            'author': post['data']['author'],
            'subreddit': post['data']['subreddit'],
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'url': post['data']['url'],
            'media': post['data']['media'],
        }, index=[0])
        
        df = pd.concat((df, post_df))

    return df.reset_index(drop=True)