import random
import Reddit
import pickle
import argparse
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
        submissions = imageScrapperReddit.Get("top")

        # Checks to make sure the Get function returns a list
        # Prints error message if it doesn't
        if isinstance(submissions, int):
            print(f"Error! Function returned {submissions}")
        else:
            await ctx.send(random.choice(submissions))

    elif parsedArgs[0] == "hot":
        submissions = imageScrapperReddit.Get("hot")

        # Checks to make sure the Get function returns a list
        # Prints error message if it doesn't
        if isinstance(submissions, int):
            print(f"Error! Function returned {submissions}")
        else:
            await ctx.send(random.choice(submissions))
    elif parsedArgs[0] == "refresh":
        await ctx.send("```Refreshing the cache...```")

        # Checks to make sure there is a second argument
        # Sends back an error message if there isn't
        try:
            returnValue = imageScrapperReddit.RefreshCache(parsedArgs[1])
            print(f"Attempting to refresh the {parsedArgs[1]} cache...")

            # Checks to make sure returnValue is 0
            # If returnValue is -1, there was an error trying to get the posts
            # If returnValue is -2, the second argument is not a valid cache
            if returnValue == 0:
                await ctx.send("```Finished refreshing the cache!```")
                print("pog it all went well, and cache was refreshed")
            elif returnValue == -1:
                await ctx.send("```There was an error while trying to retrieve the posts!```")
                print("yikes there was an error when trying to get the posts")
            elif returnValue == -2:
                await ctx.send(f"```\"{parsedArgs[1]}\" is not a valid cache!\nSupported options:\n- top\n- hot```")
                print("smh the user never supplied a valid cache")
        except:
            await ctx.send("```A cache argument was never supplied!```")
            print("smh user never even supplied a cache argument")
    else:
        await ctx.send(f"```\"{parsedArgs[0]}\" is not a supported argument of the command \".reddit\".```")


# ".help" command
@bot.command(aliases=["usage"])
async def help(ctx):
    await ctx.send("Usage:"
                   "\nTo query an image from Reddit:"
                   "\n```.reddit <top or hot>```"
                   "\nTo refresh the cache (only use if you are seeing a lot of images get reused):"
                   "\n```.reddit refresh <top or hot>```")


# Tries to use the discord token
# If there is an error, the script exits with code -1
try:
    bot.run(options[0])
except:
    print("Discord bot token isn't valid.")
    exit(-1)
