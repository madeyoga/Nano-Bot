from listener.core.image import Subreddits, Reddit

if __name__ == "__main__":
    reddit_client = Reddit()
    submission = reddit_client.search_get_post("fate abby")
    print(submission.title, submission.url)
