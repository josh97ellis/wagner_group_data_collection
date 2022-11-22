from datetime import datetime, timedelta
import yaml
import spacy
import re

# Imports from custom modules
from reddit import MyRedditAPI
from database.connection import db_connect


def extract_data():
    """
    Extracts data from reddit and returns all posts
    from yesterday
    """
    # Get Credentials
    with open('C:/Users/Josh Ellis/Documents/programming/projects/wagner-group-data-collection/config.yaml', 'r') as f:
        credentials = yaml.safe_load(f)

    # Start a Reddit API Session
    session = MyRedditAPI(
        client_id = credentials['RedditCredentials']['CLIENT_ID'],
        secret_key = credentials['RedditCredentials']['SECRET'],
        username = credentials['RedditCredentials']['USERNAME'],
        password = credentials['RedditCredentials']['PASSWORD'],
        user_agent='MyAPI')

    # Query Data
    df = session.search_posts(
        query='Wagner Group',
        subreddit='all',
        limit=250,
        sort='new')
    
    # Filter query results for yesterday
    yesterday_utc = datetime.utcnow().date() - timedelta(days=1)
    df = df[df['created_utc'].dt.date == yesterday_utc]
    
    return df


def get_locations(df):
    """
    Extracts Location Data from post Title
    """
    nlp = spacy.load('en_core_web_sm')

    titles = df['title']

    locations = []
    for title in titles:
        doc = nlp(str(title))
        locations.append(doc.ents)
            
    df['locations'] = [re.sub("[\()]", '', str(i)) for i in locations]
    df['locations'] = df['locations'].str.rstrip(',')
    
    return df


def load_data(df):
    """
    Loads the processed reddit data to pregres database
    """
    connection, cursor = db_connect()
    insert_script = (
        """
        INSERT INTO public.reddit_mentions(
            post_id, date, author, subreddit, title, body, url, media, locations)
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    )

    for index, row in df.iterrows():
        name = row[0]
        created_utc = row[1]
        author = row[2]
        subreddit = row[3]
        title = row[4]
        selftext = row[5]
        url = row[6]
        media = row[7]
        locations = row[8]
        
        cursor.execute(
            insert_script,
            [name, created_utc, author, subreddit, title, selftext, url, media, locations]
        )
        
        connection.commit()
        
    cursor.close()
    connection.close()
    print(f'{len(df)} records inserted into database')
    

def main():
    wagner_query = extract_data()
    wagner_query = get_locations(wagner_query)
    load_data(wagner_query)


if __name__ == '__main__':
    main()
