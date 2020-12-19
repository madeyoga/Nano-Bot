from discord.ext import commands
import json
import os

from listener.core.submission import embed_submission


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

    @staticmethod
    async def reply_context(ctx, submission):
        if submission.get('post_hint') == 'image':
            await ctx.send(embed=embed_submission(submission))
        else:
            await ctx.send(submission.get('url'))
