import discord

EmbedColor = 0xeb006d


# A function for making it easier to make consistent Reddit image embeds
def redditEmbed(imageUrl, user):
        embed = discord.Embed(title=":arrow_down: Look, Hentai! :arrow_down:", color=EmbedColor)
        embed.set_author(name=f"Hentai requested by {user.name}", icon_url=user.avatar_url)
        embed.set_image(url=imageUrl)

        return embed


# A function for making error message embeds
def errorEmbed(errorMessage):
        return discord.Embed(title=errorMessage, description="Please type in `.help` to view the help screen, if you are having issues.", color=EmbedColor)
