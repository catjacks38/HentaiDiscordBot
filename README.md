# HentaiDiscordBot
## It's a discord bot, but for degenerates. 👍

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

## `.help` Usage

### `.help/.usage <base command (optional)>`
- Shows help screen of base command. 
- If there is no base command or the base command is not valid, this help screen will be show by default.
- The base commands are nhentai and reddit.
### Example:
- `.help reddit`

## `.reddit` Usage

### `.reddit <top or hot> <subreddit or subreddit index (default: hentai)>`
- Picks a random image from the top or hot section on the chosen subreddit or subreddit index.
- Defaults to r/hentai if the subreddit or subreddit index is not valid or no argument is supplied.
### Examples:
- `.reddit top hentai`
- `.reddit top 0`

### `.reddit refresh <subreddit or subreddit index (default: hentai)>`
- Refreshes the cache of the chosen subreddit or subreddit index.
- Defaults to r/hentai if the subreddit or subreddit index is not valid or no argument is supplied.
### Examples:
- `.reddit refresh hentai`
- `.reddit refresh 0`

### `.reddit subreddits`
- List all the supported subreddits.

### `.reddit favorite`
- Add a submission to your favorites. To select the submissiom, type this command, and reply to the submission embed.

### `.reddit favorites <favorites submission index>`
- Lists the first page of your favorites, or selects a favorite submission by it's index (the number on the left of the submission title) if a number is supplied.
### Example:
- `.reddit favorites 0`

### `.reddit favorites page <page number>`
- Selects the page to list your favorites.
### Example:
- `.reddit favorites page 1`

### `.reddit favorites random`
- Selects a random submission from your favorites.

### `.reddit favorites remove <favorites submission index>`
- Removes a favorite submission of favorites submission index (the number on the left of the submission title) from your favorites.
### Example:
- `.reddit favorites remove 0`

### `.reddit favorites clear`
- Clears **all** of your favorites.

## `.nhentai` Usage

### `.nhentai random`
- Picks a random doujin of the user's selected language.
- This command doesn't ban or require any tags saved by you.
### Example:
- `.nhentai random`

### `.nhentai set <parameters>`
- Sets your saved tags used for querying. 
- The supported keywords are required, banned, and language.
- Note: You don't need to supply every keyword, and each tag is seperated by ", ".
- Another note: The language keyword only takes in one language, so don't do `language=english, japanese`
### Examples:
- `.nhentai set required=paizuri, story arc banned=netorare, harem language=english`
  - (required, banned, and language will be set)
- `.nhentai set required=paizuri` 
  - (Only required gets set. The rest of the saved tags don't change.)

### `.nhentai append <parameters>`
- Appends the tags in parameters to your saved tags.
- This command is used in the same way that `.nhentai set` is used.
- Note: Only the required and banned keywords work for this.
### Examples:
- `.nhentai append required=paizuri, story arc banned=netorare, harem` 
  - (Appends [paizuri, story arc] to your saved required tags and [netorare, harem] to your saved banned tags)
- `.nhentai append required=paizuri, story arc` 
  - (Appends [paizuri, story arc] to your saved tags)

### `.nhentai query <search query (optional)>`
- Queries NHentai of search query plus the user's saved tags
### Example:
- `.nhentai query my friend came back from the future to fuck me`

### `.nhentai list`
- List all of your saved tags.

### `.nhentai remove <parameters>`
- Removes tags of the user's saved tags (doesn't remove a saved language though; use `.nhentai clear language` for that)
### Examples:
- `.nhentai remove required=paizuri banned=netorare`
- `.nhentai remove required=paizuri, story arc banned=netorare, mind control`

### `.nhentai clear <saved tag (optional)>`
- Clears all of your saved tags, unless if a saved tag is supplied (can only be required, banned, or language).
### Examples:
- `.nhentai clear required`
  - (Your saved required tags are cleared)
- `.nhentai clear`
  - (All of your saved tags are cleared)
