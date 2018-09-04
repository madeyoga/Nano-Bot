from nineapi.nineapi.client import  Client, APIException
import os
import random

import praw

class Sections:
    ANIME_MANGA = 32
    WTF         = 4
    SAVAGE      = 45
    KPOP        = 34
    COMIC       = 17

class Gag:
    def __init__(self):
        self.gag_client = Client()
        self.gag_client.log_in(str( os.environ.get('GAG_USERNAME')), str(os.environ.get('GAG_PASSWORD')))

    def get_post_from(self, group_id):
        post = random.choice( 
            self.gag_client.get_posts(
                group=group_id, 
                count=50, 
                type_='hot', 
                entry_types=['photo', 'animated']
            )
        )
        return post

class Subreddits:
    MEMES           = "memes"
    DANKMEMES       = "dankmemes"
    WTF             = "wtf"
    GRANDORDER      = "grandorder"
    WAIFU           = "Waifu"
    SCATHACH        = "scathach"
    FGOFANART       = "FGOfanart"
    ANIME           = "anime"
    ANIMEMES        = "Animemes"
    AWWNIME         = "awwnime"
    AZURELANE       = "AzureLane"
    TSUNDERES       = "Tsunderes"      
    ANIMEWALLPAPER  = "Animewallpaper"  # ANIME WALLPAPER ARTS
    MOESCAPE        = "Moescape"        # ANIME WALLPAPER ARTS

class Reddit:
    def __init__(self):
        self.reddit = praw.Reddit (
            client_id     = str(os.environ.get('REDDIT_CLIENT_ID')),
            client_secret = str(os.environ.get('REDDIT_CLIENT_SECRET')),
            user_agent    = str(os.environ.get('REDDIT_USER_AGENT'))
        )
    
    def get_submission(self, subreddit):
        submissions = list(self.reddit.subreddit(subreddit).hot())
        while True:
            submission = random.choice(submissions)
            if not submission.stickied and '.' in str(submission.url)[-5:]:
                break
        return submission
