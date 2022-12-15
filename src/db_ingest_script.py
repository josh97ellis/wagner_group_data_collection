from datetime import datetime, timedelta
from dotenv import dotenv_values

# Imports from custom modules
from reddit import MyRedditAPI
from database import db_connect
from processing import (
    clean_text,
    EntityRecognition
)

config = dotenv_values('.env')

CLIENT=config.get('CLIENT_ID')
SECRET_KEY=config.get('SECRET')
USERNAME=config.get('USERNAME')
PASSWORD=config.get('PASSWORD')


def extract_data():
    """
    Extracts data from reddit and returns all posts
    from yesterday
    """
    session = MyRedditAPI(
        client_id=CLIENT,
        secret_key=SECRET_KEY,
        username=USERNAME,
        password=PASSWORD,
        user_agent='MyApiTest'
    )

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
    

def load_data(df):
    """
    Loads the processed reddit data to pregres database
    """
    connection, cursor = db_connect()
    insert_script = (
        """
        INSERT INTO public.reddit_posts(
            post_id, date, author, subreddit, title, body, media_url, post_url, locations, organizations, people)
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    )

    for index, row in df.iterrows():
        name = row[0]
        created_utc = row[1]
        author = row[2]
        subreddit = row[3]
        title = row[4]
        selftext = row[5]
        media_url = row[6]
        post_url = row[7]
        locations = row[8]
        organizations = row[9]
        people = row[10]
        
        cursor.execute(
            insert_script,
            [name, created_utc, author, subreddit, title, selftext, media_url, post_url, locations, organizations, people]
        )
        
        connection.commit()
        
    cursor.close()
    connection.close()
    print(f'{len(df)} records inserted into database')
    

def main():
    wagner_query = extract_data()
    
    # Clean title and selftext fields
    wagner_query = clean_text(wagner_query, ['title', 'selftext'])
    
    # Get locations, organizations, and People's names from title
    wagner_ner = EntityRecognition(wagner_query, 'title')
    wagner_query['locations'] = wagner_ner.get_gpe()
    wagner_query['organizations'] = wagner_ner.get_org()
    wagner_query['people'] = wagner_ner.get_person()
    
    load_data(wagner_query)


if __name__ == '__main__':
    main()
