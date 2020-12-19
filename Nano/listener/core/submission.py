from listener.core.custom.embed import CustomEmbed


def embed_submission(submission):
    embed = CustomEmbed()

    author = submission.get('author')
    # author_icon = submission.get('author_icon_url')
    if author is None:
        author = "Unknown"
        # author_icon = ""

    embed.set_author(name=author,
                     icon_url="https://cdn4.iconfinder.com/data/icons/social-messaging-ui-color-shapes-2-free/128"
                              "/social-reddit-circle-512.png",
                     url=submission.get('permalink'))
    # embed.title = submission.get('subreddit_name_prefixed')
    embed.description = f"**[{submission.get('title')}]({submission.get('permalink')})**"
    embed.add_field(name=":arrow_up: Upvotes",
                    value=submission.get('score'),
                    inline=True)
    embed.add_field(name=":art: Original",
                    value=":white_check_mark:" if submission.get('original_content') else ":x:",
                    inline=True)
    embed.set_image(url=submission.get('url'))
    embed.set_footer(text=submission.get('subreddit_name_prefixed'))

    return embed
