import Utils
import random
import Reddit
import Nhentai
import pickle
import argparse
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=".", help_command=None)
parser = argparse.ArgumentParser(description="discord bot go brrrr")
options = []

parser.add_argument("--discordToken", "-d", help="Discord bot token.")
parser.add_argument("--redditID", "-i", help="Your reddit client ID.")
parser.add_argument("--redditSecret", "-s", help="Your reddit client secret.")

args = parser.parse_args()

# Attempts to read "options.cfg"
# If reading "options.cfg" is not successful, it will print the error, and exit the program with the code of -1
if args.discordToken and args.redditID and args.redditSecret:
    with open("options.cfg", "wb") as configFile:
        pickle.dump([args.discordToken, args.redditID, args.redditSecret], configFile)

    with open("options.cfg", "rb") as configFile:
        options = pickle.load(configFile)
else:
    try:
        with open("options.cfg", "rb") as configFile:
            options = pickle.load(configFile)
            if len(options) != 3:
                print("Missing options in \"options.cfg\", or missing arguments.")
                exit(-1)
    except FileNotFoundError as e:
        print("\"options.cfg\" was not found.")
        exit(-1)

imageScrapperReddit = Reddit.ImageScrapper(options[1], options[2])
nhentaiGrabber = Nhentai.NHentaiGrabber()


# Function to help with getting submissions
def getSubmissions(server, parsedArgs, section):
    # Checks if the seconds argument is a string name of the subreddit or an index of the subreddit
    # If it is neither, it will be defaulted to r/hentai
    try:
        parsedArgs[1]
        try:
            submissions = imageScrapperReddit.Get(server, imageScrapperReddit.subreddits[int(parsedArgs[1])], section)
        except:
            submissions = imageScrapperReddit.Get(server, parsedArgs[1], section)
    except:
        parsedArgs.append("hentai")
        submissions = imageScrapperReddit.Get(server, parsedArgs[1], section)

    # Checks to make sure the Get function returns a list
    # Prints error message if it doesn't
    if isinstance(submissions, int):
        print(f"Error! Function returned {submissions}")
        return submissions

    else:
        # If submissions length is more than zero, a random submission will be chosen and removed from the submissions
        # Else, The cache will be refreshed, then a random submission will be chosen and removed from the submissions
        if len(submissions) > 0:
            choice = random.choice(submissions)
            
            imageScrapperReddit.Remove(server, parsedArgs[1], "top", choice)
            imageScrapperReddit.Remove(server, parsedArgs[1], "hot", choice)
        else:
            imageScrapperReddit.RefreshCache(server, parsedArgs[1], section)
            submissions = imageScrapperReddit.Get(server, parsedArgs[1], section)

            choice = random.choice(submissions)
            
            imageScrapperReddit.Remove(server, parsedArgs[1], "top", choice)
            imageScrapperReddit.Remove(server, parsedArgs[1], "hot", choice)

        return choice


# Prints a ready message once the bot is ready
@bot.event
async def on_ready():
    print("lol bot is ready")


# ".reddit" command
@bot.command()
async def reddit(ctx, *, args):
    parsedArgs = args.split(" ")

    # Checks if the first argument is valid
    # Sends back error if the argument is invalid

    # .reddit top <subreddit or subreddit index>
    if parsedArgs[0] == "top":
        # If there is an error trying to display the Reddit embed, remove the submission, and repeat until there is no error
        while 1:
            choice = getSubmissions(ctx.guild, parsedArgs, "top")

            try:
                await ctx.send(embed=Utils.redditEmbed(choice))
                break
            except:
                pass

    # .reddit hot <subreddit or subreddit index>
    elif parsedArgs[0] == "hot":
        # If there is an error trying to display the Reddit embed, remove the submission, and repeat until there is no error
        while 1:
            choice = getSubmissions(ctx.guild, parsedArgs, "hot")

            try:
                await ctx.send(embed=Utils.redditEmbed(choice))
                break
            except:
                pass

    # .reddit refresh <subreddit name or subreddit index>
    elif parsedArgs[0] == "refresh":

        embed = discord.Embed(title="Refreshing the cache...", color=Utils.EmbedColor)
        embed.set_author(name=f"Cache refresh requested by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)

        # Checks if the seconds argument is a string name of the subreddit or an index of the subreddit
        # If it is nether, it will be defaulted to r/hentai
        try:
            parsedArgs[1]
            try:
                topReturn = imageScrapperReddit.RefreshCache(ctx.guild, imageScrapperReddit.subreddits[int(parsedArgs[1])], "top")
                hotReturn = imageScrapperReddit.RefreshCache(ctx.guild, imageScrapperReddit.subreddits[int(parsedArgs[1])], "hot")
            except:
                topReturn = imageScrapperReddit.RefreshCache(ctx.guild, parsedArgs[1], "top")
                hotReturn = imageScrapperReddit.RefreshCache(ctx.guild, parsedArgs[1], "hot")
        except:
            parsedArgs.append("hentai")
            topReturn = imageScrapperReddit.RefreshCache(ctx.guild, parsedArgs[1], "top")
            hotReturn = imageScrapperReddit.RefreshCache(ctx.guild, parsedArgs[1], "hot")

        # Checks to make sure returnValue is 0
        # If returnValue is -1, there was an error trying to get the posts
        # If returnValue is -2, the second argument is not a valid cache
        if hotReturn == 0 and topReturn == 0:

            await ctx.send(
                embed=discord.Embed(
                    title="It seems to have all went well!",
                    description=f"The cache has been refreshed!",
                    color=Utils.EmbedColor
                )
            )

        elif hotReturn == -1 or topReturn == -1:

            await ctx.send(
                embed=discord.Embed(
                    title="There was an error when trying to retrieve the posts!",
                    description="This either means Reddit is down or the Reddit web app is broke.",
                    color=Utils.EmbedColor
                )
            )

    # .reddit subreddits
    elif parsedArgs[0] == "subreddits":
        await ctx.send(embed=Utils.supportedSubredditsEmbed(imageScrapperReddit.subreddits))

    else:
        await ctx.send(embed=Utils.errorEmbed(f"\"{parsedArgs[0]}\" is not a valid argument for `.reddit`!"))


# .nhentai command
@bot.command()
async def nhentai(ctx, *, args):
    parsedArgs = args.split(" ")

    # ".nhentai random"
    if parsedArgs[0] == "random":
        # Gets the language of the user, and gets a random doujin of that language
        _, _, lang = nhentaiGrabber.get(ctx.author)
        returnValue = nhentaiGrabber.query("", None, None, lang)

        # If the query failed, send an error message
        # Else, send the doujin
        if returnValue == -1:
            await ctx.send(embed=Utils.errorEmbed("There was an error while querying NHentai!"))
        else:
            cover, doujin = returnValue
            await ctx.send(embed=Utils.doujinEmbed(cover, doujin))

    # .nhentai query <search query>
    elif parsedArgs[0] == "query":
        # Gets the required, banned, and language tags of the user, and queries NHentai with those tags and search query (if specified)
        required, banned, lang = nhentaiGrabber.get(ctx.author)
        returnValue = nhentaiGrabber.query(args[len("query "):], required, banned, lang)

        # If the query failed, send an error message
        # Else, send the doujin
        if returnValue == -1:
            await ctx.send(embed=Utils.errorEmbed("There was an error while querying NHentai!"))
        elif returnValue == -2:
            await ctx.send(embed=Utils.errorEmbed("No results found!"))
        else:
            cover, doujin = returnValue
            await ctx.send(embed=Utils.doujinEmbed(cover, doujin))

    # .nhentai set <parameters>
    elif parsedArgs[0] == "set":
        # Parses the parameters, and sets the user's saved tags to them
        required, banned, lang = Utils.nhentaiParseKeys(args)
        returnValue = nhentaiGrabber.set(ctx.author, required, banned, lang)

        if returnValue == -1:
            await ctx.send(embed=Utils.errorEmbed("One or more of the required tags selected are banned!"))
        else:
            await ctx.send(embed=discord.Embed(title="Your saved tags have been set.", color=Utils.EmbedColor))

    # .nhentai append <parameters>
    elif parsedArgs[0] == "append":
        # Parses the parameters
        newRequired, newBanned, _ = Utils.nhentaiParseKeys(args)

        # Gets the saved tags
        required, banned, _ = nhentaiGrabber.get(ctx.author)

        # If the required keyword is supplied
        if newRequired:
            # If required is saved, append newRequired to it
            # Else, set required to newRequired
            if required:
                required += newRequired
            else:
                required = newRequired

        # If the banned keyword is supplied
        if newBanned:
            # If banned is saved, append newBanned to it
            # Else, set banned to newBanned
            if banned:
                banned += newBanned
            else:
                banned = newBanned

        # Saves the newly appended tags
        nhentaiGrabber.set(ctx.author, required, banned, None)

        await ctx.send(embed=discord.Embed(title="Appended to your saved tags.", color=Utils.EmbedColor))

    # .nhentai list
    elif parsedArgs[0] == "list":
        # Gets all of the saved tags of the user
        required, banned, lang = nhentaiGrabber.get(ctx.author)

        # Creates an embed to display the tags
        # If the tag is None, the string "None" will be sent, instead of an exception being thrown
        embed = discord.Embed(title=f"Saved tags of {ctx.author.name}", color=Utils.EmbedColor)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="Required: ", value="None" if not required else "".join(map(lambda x: str(x) + ", ", required))[:-2], inline=False)
        embed.add_field(name="Banned: ", value="None" if not banned else "".join(map(lambda x: str(x) + ", ", banned))[:-2], inline=False)
        embed.add_field(name="Language: ", value="None" if not lang else lang, inline=False)

        await ctx.send(embed=embed)

    # .nhentai clear
    elif parsedArgs[0] == "clear":
        try:
            # If parsedArgs[1] is supplied, and it is equal to either required, banned, or language
            # Then clear the user's saved tag(s) of parsedArgs[1]
            if parsedArgs[1] in ["required", "banned", "language"]:
                nhentaiGrabber.clear(ctx.author, parsedArgs[1])

                await ctx.send(embed=discord.Embed(title=f"The saved tag(s) of {parsedArgs[1]} have been cleared.", color=Utils.EmbedColor))

            # If parsedArgs[1] is supplied, but it isn't a valid saved user tag
            # Send an error message
            else:
                await ctx.send(embed=Utils.errorEmbed(f"\"{parsedArgs[1]}\" is not a valid saved tag. It must be, required, banned, or language."))
        except:
            # If parsedArgs[1] was never supplied
            nhentaiGrabber.clear(ctx.author)
            await ctx.send(embed=discord.Embed(title="All of your saved tag(s) have been cleared."))


# .help <base command (optional)> command
@bot.command(aliases=["usage"])
async def help(ctx, *, args=""):
    # Creates fancy help screen embed, so it looks like I know what im doing

    embed = discord.Embed(title="Help and Usage", color=Utils.EmbedColor)

    if args == "reddit":
        embed.add_field(
            name=".reddit <top or hot> <subreddit or subreddit index (default: hentai)>",
            value="Picks a random image from the top or hot section on the chosen subreddit or subreddit index."
                  "\nDefaults to r/hentai if the subreddit or subreddit index is not valid or no argument is supplied."
                  "\nExamples:"
                  "\n`.reddit top hentai`"
                  "\n`.reddit top 0`",
            inline=False
        )
        embed.add_field(
            name=".reddit refresh <subreddit or subreddit index (default: hentai)>",
            value="Refreshes the cache of the chosen subreddit or subreddit index."
                  "\nDefaults to r/hentai if the subreddit or subreddit index is not valid or no argument is supplied."
                  "\nExamples:"
                  "\n`.reddit refresh hentai`"
                  "\n`.reddit refresh 0`",
            inline=False
        )
        embed.add_field(
            name=".reddit subreddits",
            value="Lists all the supported subreddits.",
            inline=False
        )

    elif args == "nhentai":
        embed.add_field(
            name=".nhentai random",
            value="Picks a random doujin of the user's selected language. "
                  "This command doesn't ban or require any tags saved by you."
                  "\nExample:"
                  "\n`.nhentai random`",
            inline=False
        )
        embed.add_field(
            name=".nhentai set <parameters>",
            value="Sets your saved tags used for querying. The supported keywords are required, banned, and language."
                  "\n Note: You don't need to supply every keyword, and each tag is seperated by \", \"."
                  "\n Another note: The language keyword only takes in one language, so don't do `language=english, japanese`."
                  "\nExamples:"
                  "\n`.nhentai set required=paizuri, story arc banned=netorare, harem language=english`"
                  "\n (required, banned, and language will be set)"
                  "\n`.nhentai set required=paizuri`"
                  "\n (Only required gets set. The rest of the saved tags don't change.)",
            inline=False
        )
        embed.add_field(
            name=".nhentai append <parameters>",
            value="Appends the tags in parameters to your saved tags. "
                  "This command is used in the same way that `.nhentai set` is used."
                  "\nNote: Only the required and banned keywords work for this."
                  "\nExamples:"
                  "\n`.nhentai append required=paizuri, story arc banned=netorare, harem`"
                  "\n(Appends [paizuri, story arc] to your saved required tags and [netorare, harem] to your saved banned tags)"
                  "\n`.nhentai append required=paizuri, story arc`"
                  "\n(Appends [paizuri, story arc] to your saved tags)",
            inline=False
        )
        embed.add_field(
            name=".nhentai query <search query (optional)>",
            value="Queries NHentai of search query plus the user's saved tags"
                  "\nExample:"
                  "\n`.nhentai query my friend came back from the future to fuck me`",
            inline=False
        )
        embed.add_field(
            name=".nhentai list",
            value="List all of your saved tags.",
            inline=False
        )
        embed.add_field(
            name=".nhentai clear <saved tag (optional)>",
            value="Clears all of your saved tags, unless if a saved tag is supplied (can only be required, banned, or language)."
                  "\nExamples:"
                  "\n`.nhentai clear required`"
                  "\n(Your saved required tags are cleared)"
                  "\n`.nhentai clear`"
                  "\n(All of your saved tags are cleared)",
            inline=False
        )

    else:
        embed.add_field(
            name=".help/.usage <base command (optional)>",
            value="Shows help screen of base command. "
                  "If there is no base command or the base command is not valid, this help screen will be show by default."
                  "\nThe base commands are nhentai and reddit."
                  "\nExample:"
                  "\n`.help reddit`",
            inline=False
        )

    embed.add_field(
        name="Project Homepage:",
        value="[https://github.com/catjacks38/HentaiDiscordBot](url)",
        inline=False
    )
    embed.add_field(
        name="Submit any Bugs or Feature Requests Here:",
        value="[https://github.com/catjacks38/HentaiDiscordBot/issues](url)",
        inline=False
    )

    await ctx.send(embed=embed)


# Tries to use the discord token
# If there is an error, the script exits with code -1
try:
    bot.run(options[0])
except:
    print("Discord bot token isn't valid.")
    exit(-1)
