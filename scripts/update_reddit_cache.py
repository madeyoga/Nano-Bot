import os
import praw

class Subreddits:
    MEMES = "memes"
    DANKMEMES = "dankmemes"
    WTF = "wtf"
    GRANDORDER = "grandorder"
    WAIFU = "Waifu"
    SCATHACH = "scathach"
    FGOFANART = "FGOfanart"
    ANIME = "anime"
    ANIMEMES = "Animemes"
    AWWNIME = "awwnime"
    AZURELANE = "AzureLane"
    TSUNDERES = "Tsunderes"
    ANIMEWALLPAPER = "Animewallpaper"  # ANIME WALLPAPER ARTS
    MOESCAPE = "Moescape"  # ANIME WALLPAPER ARTS
    MAMARAIKOU = "MamaRaikou"
    SABER = "Saber"
    FGOCOMICS = "FGOcomics"
    FATEPRISMAILLYA = "FatePrismaIllya"
    ILLYASVIEL = "Illyasviel"

reddit = praw.Reddit(
    client_id=os.environ['REDDIT_CLIENT_ID'],
    client_secret=os.environ['REDDIT_CLIENT_SECRET'],
    user_agent=os.environ['REDDIT_USER_AGENT']
)

submissions = list(reddit.subreddit(Subreddits.TSUNDERES).hot())

for submission in submissions:
    # Post hint & url
    print(submission.__dict__)
    break
##    print(submission.url,
##          submission.is_self,
##          submission.over_18,
##          submission.stickied)
