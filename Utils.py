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


def nhentaiParseKeys(args):
        requiredIDX = args.find("required=")
        bannedIDX = args.find("banned=")

        if requiredIDX == -1:
                requiredTags = None
        else:
                requiredTags = args[requiredIDX + len("required="):bannedIDX - 1 if bannedIDX > requiredIDX else len(args)].split(", ")

        if bannedIDX == -1:
                bannedTags = None
        else:
                bannedTags = args[bannedIDX + len("banned="):requiredIDX - 1 if requiredIDX > bannedIDX else len(args)].split(", ")

        return requiredTags, bannedTags


def doujinEmbed(cover, doujin):
        embed = discord.Embed(title=doujin.title, description=f"[https://nhentai.net/g/{doujin.id}](url)", color=EmbedColor)
        embed.set_image(url=cover)
        embed.add_field(name="Artists", value="".join(map(lambda x: str(x) + ", ", doujin.artists))[:-2], inline=False)
        embed.add_field(name="Tags", value="".join(map(lambda x: str(x) + ", ", doujin.tags))[:-2], inline=False)
        embed.add_field(name="Language Tags", value="".join(map(lambda x: str(x) + ", ", doujin.languages))[:-2], inline=False)
        embed.set_footer(text=f"{doujin.total_pages} pages.")

        return embed
