from listener.core.subreddit import subreddit_dictionary
import praw
import os
import json
from random import shuffle


reddit = praw.Reddit(
    client_id=os.environ['REDDIT_CLIENT_ID'],
    client_secret=os.environ['REDDIT_CLIENT_SECRET'],
    user_agent=os.environ['REDDIT_USER_AGENT']
)

for key in subreddit_dictionary:
    subreddit_name = subreddit_dictionary.get(key)

    submissions = list(reddit.subreddit(subreddit_name).hot())
    shuffle(submissions)

    dump_list = []
    for submission in submissions:
        temp = submission.__dict__
        if submission.author is not None:
            author = submission.author.name
        else:
            author = None

        permalink = temp.get('permalink')

        submission_dict = {
            'title': submission.title,
            'author': author,
            'subreddit_name_prefixed': temp.get('subreddit_name_prefixed'),
            'post_hint': temp.get('post_hint'),
            'url': temp.get('url'),
            'url_overridden_by_dest': temp.get('url_overridden_by_dest'),
            'over_18': submission.over_18,
            'permalink': f"https://www.reddit.com{permalink}"
        }
        dump_list.append(submission_dict)

    filepath = f'listener/cache/{subreddit_name}.json'
    with open(filepath, 'w+') as file:
        json.dump(dump_list, fp=file, indent=2)

    print(key, "dumped to", filepath)
