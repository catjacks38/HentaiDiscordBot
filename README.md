# HentaiDiscordBot
## It's a discord bot, but for degenerates. 👍

### Disclaimer: This bot is still a WIP project. It still is missing a lot of functionality. I would not suggest you add this to your server just yet.

## Script Requirements
- discord.py
- praw

## CLI Usage
To start the bot, type in 
- Windows: `python bot.py -d <discord bot token> -i <reddit web app ID> -s <reddit web app secret token>`
- Linux: `python3 bot.py -d <discord bot token> -i <reddit web app ID> -s <reddit web app secret token>`

## Bot Usage
`.reddit <top or hot>`
- Shows a random image from the choosen section of reddit (top or hot)

`.reddit refresh <top or hot>`
- Refreshes the top or hot cache of image links. Use this command if you are starting to see a lot of image get repeated.
- The top cache is automatically refreshed every 10 minutes
- The hot cache is automatically refreshed every 3.5 minutes
