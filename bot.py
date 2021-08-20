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
nhentaiScrapper = Nhentai.NhentaiScrapper()


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
        # Checks if the seconds argument is a string name of the subreddit or an index of the subreddit
        # If it is nether, it will be defaulted to r/hentai
        try:
            parsedArgs[1]

            try:
                submissions = imageScrapperReddit.Get(ctx.guild, imageScrapperReddit.subreddits[int(parsedArgs[1])], "top")
            except:
                submissions = imageScrapperReddit.Get(ctx.guild, parsedArgs[1], "top")
        except:
            parsedArgs.append("hentai")
            submissions = imageScrapperReddit.Get(ctx.guild, parsedArgs[1], "top")

        # Checks to make sure the Get function returns a list
        # Prints error message if it doesn't
        if isinstance(submissions, int):
            print(f"Error! Function returned {submissions}")
        else:
            # If submissions length is more than zero, a random submission will be chosen and removed from the submissions
            # Else, The cache will be refreshed, then a random submission will be chosen and removed from the submissions
            if len(submissions) > 0:
                choice = random.choice(submissions)
                imageScrapperReddit.Remove(ctx.guild, parsedArgs[1], "top", choice)
            else:
                imageScrapperReddit.RefreshCache(ctx.guild, parsedArgs[1], "top")
                submissions = imageScrapperReddit.Get(ctx.guild, parsedArgs[1], "top")

                choice = random.choice(submissions)
                imageScrapperReddit.Remove(ctx.guild, parsedArgs[1], "top", choice)

            await ctx.send(embed=Utils.redditEmbed(choice))

    # .reddit hot <subreddit or subreddit index>
    elif parsedArgs[0] == "hot":
        # Checks if the seconds argument is a string name of the subreddit or an index of the subreddit
        # If it is nether, it will be defaulted to r/hentai
        try:
            parsedArgs[1]
            try:
                submissions = imageScrapperReddit.Get(ctx.guild, imageScrapperReddit.subreddits[int(parsedArgs[1])], "hot")
            except:
                submissions = imageScrapperReddit.Get(ctx.guild, parsedArgs[1], "hot")
        except:
            parsedArgs.append("hentai")
            submissions = imageScrapperReddit.Get(ctx.guild, parsedArgs[1], "hot")

        # Checks to make sure the Get function returns a list
        # Prints error message if it doesn't
        if isinstance(submissions, int):
            print(f"Error! Function returned {submissions}")
        else:
            # If submissions length is more than zero, a random submission will be chosen and removed from the submissions
            # Else, The cache will be refreshed, then a random submission will be chosen and removed from the submissions
            if len(submissions) > 0:
                choice = random.choice(submissions)
                imageScrapperReddit.Remove(ctx.guild, parsedArgs[1], "hot", choice)
            else:
                imageScrapperReddit.RefreshCache(ctx.guild, parsedArgs[1], "hot")
                submissions = imageScrapperReddit.Get(ctx.guild, parsedArgs[1], "hot")

                choice = random.choice(submissions)
                imageScrapperReddit.Remove(ctx.guild, parsedArgs[1], "hot", choice)

            await ctx.send(embed=Utils.redditEmbed(choice))

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


# ".nhentai" command
@bot.command()
async def nhentai(ctx, *, args):
    parsedArgs = args.split(" ")

    if parsedArgs[0] == "random":
        _, _, lang = nhentaiScrapper.get(ctx.author)
        returnValue = nhentaiScrapper.query("", None, None, lang)

        if returnValue == -1:
            await ctx.send(embed=Utils.errorEmbed("There was an error while querying Nhentai!"))
        else:
            cover, doujin = returnValue
            await ctx.send(embed=Utils.doujinEmbed(cover, doujin))

    elif parsedArgs[0] == "query":

        required, banned, lang = nhentaiScrapper.get(ctx.author)

        returnValue = nhentaiScrapper.query(args[len("query "):], required, banned, lang)

        if returnValue == -1:
            await ctx.send(embed=Utils.errorEmbed("There was an error while querying Nhentai!"))
        else:
            cover, doujin = returnValue
            await ctx.send(embed=Utils.doujinEmbed(cover, doujin))

    elif parsedArgs[0] == "set":
        required, banned, lang = Utils.nhentaiParseKeys(args)

        nhentaiScrapper.set(ctx.author, required, banned, lang)

    elif parsedArgs[0] == "list":
        required, banned, lang = nhentaiScrapper.get(ctx.author)

        embed = discord.Embed(title=f"Saved tags of {ctx.author.name}", color=Utils.EmbedColor)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="Required: ", value="None" if not required else "".join(map(lambda x: str(x) + ", ", required))[:-2], inline=False)
        embed.add_field(name="Banned: ", value="None" if not banned else "".join(map(lambda x: str(x) + ", ", banned))[:-2], inline=False)
        embed.add_field(name="Language: ", value="None" if not lang else lang, inline=False)

        await ctx.send(embed=embed)

    elif parsedArgs[0] == "clear":
        nhentaiScrapper.clear(ctx.author)


# ".help" command
@bot.command(aliases=["usage"])
async def help(ctx):
    # Creates fancy help screen embed, so it looks like I know what im doing

    embed = discord.Embed(
        title="Help and Usage",
        color=Utils.EmbedColor
    )

    embed.add_field(name=".help/.usage", value="Shows this help screen.", inline=False)
    embed.add_field(
        name=".reddit <top or hot> <subreddit or subreddit index>",
        value="Picks a random image from the top or hot section on the chosen subreddit or subreddit index."
              "\nDefaults to r/hentai if the subreddit or subreddit index is not valid or no argument is supplied."
              "\nExamples:"
              "\n`.reddit top hentai`"
              "\n`.reddit top 0`",
        inline=False
    )
    embed.add_field(
        name=".reddit refresh <subreddit or subreddit index>",
        value="Refreshes the cache of the chosen subreddit or subreddit index."
              "\nDefaults to r/hentai if the subreddit or subreddit index is not valid or no argument is supplied."
              "\nExamples:"
              "\n`.reddit refresh hentai`"
              "\n`.reddit refresh 0`",
        inline=False
    )
    embed.add_field(
        name=".reddit subreddits",
        value="Lists all of the supported subreddits.",
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
