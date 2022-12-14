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
        title, selftext, media_url, and post_url}
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
            'media_url': post['data']['url'],
            'post_url': f"https://www.reddit.com{post['data']['permalink']}"
        }, index=[0])
        
        df = pd.concat((df, post_df))

    return df.reset_index(drop=True)