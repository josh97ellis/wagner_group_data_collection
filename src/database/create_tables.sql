CREATE TABLE public.reddit_mentions
(
    post_id TEXT NOT NULL,
    date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    author TEXT NOT NULL,
    subreddit TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    url TEXT,
    media TEXT,
    locations TEXT,
	PRIMARY KEY (post_id)	
)