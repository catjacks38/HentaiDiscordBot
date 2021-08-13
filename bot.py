import Utils
import random
import Reddit
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


# Prints a success message once the bot is ready
@bot.event
async def on_ready():
    print("lol bot is ready")


# ".reddit" command
@bot.command()
async def reddit(ctx, *, args):
    parsedArgs = args.split(" ")

    # Checks if the first argument is valid
    # Sends back error if the argument is invalid
    if parsedArgs[0] == "top":
        try:
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

    elif parsedArgs[0] == "hot":
        try:
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
    elif parsedArgs[0] == "refresh":

        embed = discord.Embed(title="Refreshing the cache...", color=Utils.EmbedColor)
        embed.set_author(name=f"Cache refresh requested by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)

        # Checks to make sure there is a second argument
        # Sends back an error message if there isn't
        try:
            returnValue = imageScrapperReddit.RefreshCache(parsedArgs[1], ctx.guild)
            print(f"Attempting to refresh the {parsedArgs[1]} cache...")

            # Checks to make sure returnValue is 0
            # If returnValue is -1, there was an error trying to get the posts
            # If returnValue is -2, the second argument is not a valid cache
            if returnValue == 0:

                await ctx.send(
                    embed=discord.Embed(
                        title="It seems to have all went well!",
                        description=f"The {parsedArgs[1]} cache has been refreshed!",
                        color=Utils.EmbedColor
                    )
                )

                print("pog it all went well, and cache was refreshed")
            elif returnValue == -1:

                await ctx.send(
                    embed=discord.Embed(
                        title="There was an error when trying to retrieve the posts!",
                        description="This either means Reddit is down or the Reddit web app is broke.",
                        color=Utils.EmbedColor
                    )
                )

                print("yikes there was an error when trying to get the posts")
            elif returnValue == -2:

                await ctx.send(embed=Utils.errorEmbed(f"\"{parsedArgs[1]}\" is not a valid cache!"))

                print("smh the user never supplied a valid cache")
        except:
            await ctx.send(embed=Utils.errorEmbed("A cache argument was never supplied!"))
            print("smh user never even supplied a cache argument")
    else:
        await ctx.send(embed=Utils.errorEmbed(f"\"{parsedArgs[0]}\" is not a valid argument for `.reddit`!"))


# ".help" command
@bot.command(aliases=["usage"])
async def help(ctx):
    # Creates fancy help screen embed, so it looks like I know what im doing

    embed = discord.Embed(
        title="Help and Usage",
        color=Utils.EmbedColor
    )

    embed.add_field(name=".help/.usage", value="Shows this help screen", inline=False)
    embed.add_field(name=".reddit <top or hot>", value="Picks a random image from the top or hot section on r/hentai.", inline=False)
    embed.add_field(
        name=".reddit refresh <top or hot>",
        value="Refreshes the cache of the top or hot section.",
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
