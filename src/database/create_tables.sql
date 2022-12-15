CREATE TABLE public.reddit_mentions
(
    post_id TEXT NOT NULL,
    date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    author TEXT NOT NULL,
    subreddit TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    media_url TEXT,
    post_url TEXT,
    locations TEXT,
    organizations TEXT,
    people TEXT,
	PRIMARY KEY (post_id)	
)