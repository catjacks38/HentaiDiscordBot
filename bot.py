import random
import Reddit
import pickle
import argparse
from discord.ext import commands

bot = commands.Bot(command_prefix=".")
parser = argparse.ArgumentParser(description="discord bot go brrrr")
options = []

parser.add_argument("--discordToken", "-d", help="Discord bot token.")
parser.add_argument("--redditID", "-i", help="Your reddit client ID.")
parser.add_argument("--redditSecret", "-s", help="Your reddit client secret.")

args = parser.parse_args()

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


@bot.event
async def on_ready():
    print("lol bot is ready")


@bot.command()
async def reddit(ctx, *, args):
    if args == "top":
        submissions = imageScrapperReddit.Get("top")

        if isinstance(submissions, int):
            print(f"Error! Function returned {submissions}")
        else:
            await ctx.send(random.choice(submissions))

    elif args == "hot":
        submissions = imageScrapperReddit.Get("hot")

        if isinstance(submissions, int):
            print(f"Error! Function returned {submissions}")
        else:
            await ctx.send(random.choice(submissions))
    else:
        await ctx.send(f"\"{args}\" is not a supported argument of the command \".reddit\".")


try:
    bot.run(options[0])
except:
    print("Discord bot token isn't valid.")
    exit(-1)
