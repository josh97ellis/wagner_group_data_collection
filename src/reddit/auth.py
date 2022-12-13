import requests

class RedditAuth():
    """
    Authenticate Reddit API Sign-in Credentials  
    
    To generate a client_id and a secret_key, develope an application on reddit: https://www.reddit.com/prefs/apps
    
    PARAMS:
    --------
        - client_id: str
            - ID provided when creating the Reddit app
        - secret_key: str
            - Secret provided when creating the reddit app
        - username: str
            - Your personal Reddit Username
        - password: str
            - Your personal Reddit Password
        - user_agent: str
            - Value can be any string, i.e., "Reddit-API-Test"
    """
    def __init__(self, client_id, secret_key, username, password, user_agent):
        self.client_id = client_id
        self.secret_key = secret_key
        self.username = username
        self.password = password
        self.user_agent = user_agent
        
    def start_session(self):
        """
        Generates the OAUTH and Access Tokens to use the API
        """
        auth = requests.auth.HTTPBasicAuth(self.client_id, self.secret_key)
        login_info = {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password 
        }
        headers = {'User-Agent': self.user_agent}
        
        # Send request for OAUTH Token
        res = requests.post(
            'https://www.reddit.com/api/v1/access_token',
            auth=auth,
            data=login_info,
            headers=headers)
        
        # Get Access Token
        TOKEN = res.json()['access_token']

        # Add the token to the API Header
        headers['Authorization'] = f'bearer {TOKEN}'
        
        return headers