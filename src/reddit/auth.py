import requests

class RedditAuth():
    """
    Provide the Authentication to reddit and starts
    and API session
    """
    def __init__(self, client_id, secret_key, username, password, user_agent):
        self.client_id = client_id
        self.secret_key = secret_key
        self.username = username
        self.password = password
        self.user_agent = user_agent
        
    def start_session(self):
        # authenticate API
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