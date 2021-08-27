import discord

EmbedColor = 0xeb006d


# A function for making it easier to make consistent Reddit image embeds
def submissionEmbed(submission):
        embed = discord.Embed(title=":arrow_down: Look, Hentai! :arrow_down:", color=EmbedColor)
        embed.set_author(name=f"Hentai posted by u/{submission.author.name}", icon_url=submission.author.icon_img)
        embed.add_field(name="Submission Link:", value=f"[{submission.shortlink}](url)", inline=False)
        embed.set_image(url=submission.url)

        return embed


def submissionDataEmbed(submissionData):
        embed = discord.Embed(title=":arrow_down: Look, Hentai! :arrow_down:", color=EmbedColor)
        embed.set_author(name=f"Hentai posted by u/{submissionData.authorName}", icon_url=submissionData.authorIconUrl)
        embed.add_field(name="Submission Link:", value=f"[{submissionData.shortlink}](url)", inline=False)
        embed.set_image(url=submissionData.imageUrl)

        return embed


# A function for making error message embeds
def errorEmbed(errorMessage):
        return discord.Embed(title=errorMessage, description="Please type in `.help` to view the help screen, if you are having issues.", color=EmbedColor)


# A function for listing all of the supported subreddits
def supportedSubredditsEmbed(subreddits):
        stringList = "Index - Subreddit"

        for i, subreddit in enumerate(subreddits):
                stringList += f"\n{i} - {subreddit}"

        return discord.Embed(title="Supported subreddits", description=stringList, color=EmbedColor)


# A function for parsing the keywords for getting banned, required, and languages tags
def nhentaiParseKeys(args):
        # Attempts to find all of the keywords in args
        requiredIDX = args.find("required=")
        bannedIDX = args.find("banned=")
        langIDX = args.find("language=")

        # If that keyword index is equal to -1, than set the tag to None
        # Else, Find the closest next keyword, and stored the index of it in stopIDX
        # If the there is no next keyword, stopIDX is set to the length of args
        # Get the string indice of the end of the keyword to stopIDX
        # Split the string into a list if the tag is required or banned. This doesn't happen for the language keyword
        if requiredIDX == -1:
                requiredTags = None
        else:
                IDXList = []

                if bannedIDX > requiredIDX:
                        IDXList.append(bannedIDX)

                if langIDX > requiredIDX:
                        IDXList.append(langIDX)

                stopIDX = len(args) if len(IDXList) == 0 else min(IDXList) - 1

                requiredTags = args[requiredIDX + len("required="):stopIDX].split(", ")

        if bannedIDX == -1:
                bannedTags = None
        else:
                IDXList = []

                if requiredIDX > bannedIDX:
                        IDXList.append(requiredIDX)

                if langIDX > bannedIDX:
                        IDXList.append(langIDX)

                stopIDX = len(args) if len(IDXList) == 0 else min(IDXList) - 1

                bannedTags = args[bannedIDX + len("banned="):stopIDX].split(", ")

        if langIDX == -1:
                lang = None
        else:
                IDXList = []

                if requiredIDX > langIDX:
                        IDXList.append(requiredIDX)

                if bannedIDX > langIDX:
                        IDXList.append(bannedIDX)

                stopIDX = len(args) if len(IDXList) == 0 else min(IDXList) - 1

                lang = args[langIDX + len("language="):stopIDX]

        # If the tag(s) is empty, set the tag(s) to None
        requiredTags = None if requiredTags == [""] else requiredTags
        bannedTags = None if bannedTags == [""] else bannedTags

        return requiredTags, bannedTags, lang


# A function for making the doujin embeds
def doujinEmbed(cover, doujin):
        embed = discord.Embed(title=doujin.title, description=f"[https://nhentai.net/g/{doujin.id}](url)", color=EmbedColor)
        embed.set_image(url=cover)
        embed.add_field(name="Artists:", value="None" if len(doujin.artists) == 0 else "".join(map(lambda x: str(x) + ", ", doujin.artists))[:-2], inline=False)
        embed.add_field(name="Tags:", value="None" if len(doujin.tags) == 0 else "".join(map(lambda x: str(x) + ", ", doujin.tags))[:-2], inline=False)
        embed.add_field(name="Language Tags:", value="None" if len(doujin.languages) == 0 else "".join(map(lambda x: str(x) + ", ", doujin.languages))[:-2], inline=False)
        embed.set_footer(text=f"{doujin.total_pages} pages.")

        return embed


def favoritesListEmbed(submissions):
        embed = discord.Embed(title="Your Favorites:")

        for i, submission in enumerate(submissions):
                embed.add_field(name=f"{i} - {submission.title}", value=f"[{submission.shortlink}](url)", inline=False)

        return embed
