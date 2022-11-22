import requests
import pandas as pd
from .auth import RedditAuth
from .table import response_table


class MyRedditAPI:
    """
    This class provides a level of abstraction from the Reddit API,
    providing an easy way to pull data from the API.
    
    Instances of this class are the gateway to interacting with Reddit's API
    """
    def __init__(
        self, 
        client_id,
        secret_key,
        username,
        password,
        user_agent
    ):
        self.client_id = client_id
        self.secret_key = secret_key
        self.username = username
        self.password = password
        self.user_agent = user_agent

    def __call__(self):
        """
        Provides authorization to Reddit API. Automatically called
        in all methods of the class
        """
        authorize = RedditAuth(self.client_id, self.secret_key,
                               self.username, self.password, self.user_agent)
        return authorize.start_session()

    def search_posts(
        self,
        query: str,
        subreddit='all',
        limit=25,
        sort='relevance',
        before='',
        after=''
    ) -> pd.DataFrame():
        """
        Provides Reddit query search functionality
        
        ### Args:
            query (str):
                The query string to search for.
            subreddit (str, optional):
                The subreddit to search within. Defaults to 'all'.
            limit (int, optional):
                The number of posts to return back. Defaults to 25.
            sort (str, optional):
                Can be one of: ``"relevance"``, ``"hot"``, ``"top"``, ``"new"``, or ``"comments"``. (default: ``"relevance"``).
            before (str, optional): Takes a post fullname (t3_xxxxxx) and returns posts prior
            after (str, optional): Takes a post fullname (t3_xxxxxx) and returns posts after

        Returns:
            pd.DataFrame Object
        """
        # initialize dataframe and parameters for pulling data in loop
        data = pd.DataFrame()
        search_params = {
            'limit': limit,
            'q': query,
            'sort': sort,
            'before': before,
            'after': after
            }
        
        # Reddit API only allows for UP TO 100 posts from a single API request
        # Therefore, the limit arg is broken up into 100 limit chunks up until
        # the last chunk that is > 100. i.e., limit = 350 -> [100, 100, 100, 50].
        iteration_list = []
        while limit > 100:
            iteration_list.append('100')
            limit -= 100
        iteration_list.append(limit)

        # Run a API Search Query for each each element in the iteration list
        # The iteration_list provides the limit parameter
        for iter_limit in iteration_list:
            search_params['limit'] = iter_limit

            # Make API Request
            res = requests.get(
                url=(f'https://oauth.reddit.com/r/{subreddit}/search'),
                headers=self.__call__(),
                params = search_params
            )

            # uses the function in from table module that defines the output
            df_new = response_table(res)

            # take the final row (oldest entry)   
            row = df_new.iloc[len(df_new)-1] 
            # add/update fullname in params
            search_params['after'] = row['name']
            # append new_df to data
            data = pd.concat((data, df_new))
        
        data.sort_values(by='created_utc', ascending=False, inplace=True)
            
        return data.reset_index(drop=True)
