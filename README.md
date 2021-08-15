# HentaiDiscordBot
## It's a discord bot, but for degenerates. 👍

## Inviting the Bot to Your Server
Hopefully I don't regret giving this link out, but here it is: [Invite Link](https://discord.com/api/oauth2/authorize?client_id=873751579470233722&permissions=171799071808&scope=bot)

## Script Requirements
### Interpreter:
- Python 3
### Packages
- discord.py
- praw
- discord_variables_plugin
- Nhentai-API

## Install Script Requirements
- Windows: `pip install -r requirements.txt`
- Linux: `pip3 install -r requirements.txt`

## CLI Usage
To start the bot for the first time, type in 
- Windows: `python bot.py -d <discord bot token> -i <reddit web app ID> -s <reddit web app secret token>`
- Linux: `python3 bot.py -d <discord bot token> -i <reddit web app ID> -s <reddit web app secret token>`

To start the bot again, type in
- Windows: `python bot.py`
- Linux: `python3 bot.py`

## Bot Usage
### `.help` or `.usage`
- Shows help/usage screen

### `.reddit <top or hot> <subreddit or index>`
- Picks a random image from the top or hot section on the chosen subreddit or subreddit index.
- Defaults to r/hentai if the subreddit or subreddit index is not valid or no argument is supplied.
### Examples:
- `.reddit top hentai`
- `.reddit top 0`

### `.reddit refresh <top or hot>`
- Refreshes the cache of the chosen subreddit or subreddit index.
- Defaults to r/hentai if the subreddit or subreddit index is not valid or no argument is supplied.
### Examples:
- `.reddit refresh hentai`
- `.reddit refresh 0`
