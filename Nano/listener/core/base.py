from discord.ext import commands
import json
import os


class BaseImageCog(commands.Cog):

    def __init__(self):
        self.pools = {}

    def load_pools(self, subreddits):
        self.pools.clear()
        for key, subreddit_name in subreddits.items():
            cache_filepath = f"listener/cache/{subreddit_name}.json"
            if not os.path.exists(cache_filepath):
                continue
            with open(cache_filepath, 'r') as json_file:
                self.pools[key] = json.loads(json_file.read())
