import discord

EmbedColor = 0xeb006d


# A function for making it easier to make consistent Reddit image embeds
def redditEmbed(submission):
        embed = discord.Embed(title=":arrow_down: Look, Hentai! :arrow_down:", color=EmbedColor)
        embed.set_author(name=f"Hentai posted by u/{submission.author.name}", icon_url=submission.author.icon_img)
        embed.add_field(name="Submission Link:", value=f"[{submission.shortlink}](url)", inline=False)
        embed.set_image(url=submission.url)

        return embed


# A function for making error message embeds
def errorEmbed(errorMessage):
        return discord.Embed(title=errorMessage, description="Please type in `.help` to view the help screen, if you are having issues.", color=EmbedColor)


# A function for listing all of the supported subreddits
def supportedSubredditsEmbed(subreddits):
        stringList = "Index - Subreddit"

        for i in range(len(subreddits)):
                stringList += f"\n{i} - {subreddits[i]}"

        return discord.Embed(title="Supported subreddits", description=stringList, color=EmbedColor)
