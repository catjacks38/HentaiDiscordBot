import praw
from discord_variables_plugin import ServerVariables


# A class for scrapping the images off of subreddits
class ImageScraper:
    # The limit on how many posts to grab
    topLimit = 200
    hotLimit = 200

    # Server variables file path
    serverVarsFp = "server.vars"

    subreddits = ["hentai", "ecchi"]

    def __init__(self, clientID, clientSecret):
        # Creates bot
        self.__bot = praw.Reddit(user_agent="Image Scrapper Thing (by u/catjacks38)", client_id=clientID, client_secret=clientSecret)
        self.__serverVars = ServerVariables()

        # Tries to read the cache files
        # Creates new cache file, if it doesn't exist
        try:
            self.__serverVars.load(self.serverVarsFp)
        except:
            self.__serverVars.save(self.serverVarsFp)

    def RefreshCache(self, server, subreddit, section):

        submissions = []
        sr = "hentai"

        # Checks to see if the subreddit is valid
        # If the subreddit is not valid, it will be defaulted to r/hentai
        if subreddit in self.subreddits:
            sr = subreddit

        # Tries to get the submissions, and returns -1 if it fails
        # If section is not a valid section, the function returns -2
        try:
            if section == "top":
                posts = self.__bot.subreddit(sr).top("day", limit=self.topLimit)
            elif section == "hot":
                posts = self.__bot.subreddit(sr).hot(limit=self.hotLimit)
            else:
                return -2
        except:
            return -1

        print(f"Refreshing {section} of r/{sr}")

        for post in posts:
            url = post.url

            # Only appends the URL if it is an image URL
            if url[:18] == "https://i.redd.it/" or url[:20] == "https://i.imgur.com/":
                submissions.append(post)

        # Tries to insert data into a new key or existing key of newCache
        # Creates a new dictionary if there are no caches of sr
        try:
            newCache = self.__serverVars.get(server, sr)
            newCache[section] = submissions
        except:
            newCache = {section : submissions}

        # Saves the posts to serverVars
        self.__serverVars.set(server, sr, newCache)
        self.__serverVars.save(self.serverVarsFp)

        return 0

    def Get(self, server, subreddit, section):
        sr = "hentai"

        # Checks to see if the subreddit is valid
        # If the subreddit is not valid, it will be defaulted to r/hentai
        if subreddit in self.subreddits:
            sr = subreddit

        # If section is not a valid section, the function returns -2
        if section == "top":

            # Refreshes cache if there is no cache
            try:
                submissions = self.__serverVars.get(server, sr)
                return submissions["top"]
            except:
                pass

            returnValue = self.RefreshCache(server, sr, "top")

            # Loads the top submissions of sr, and returns the submissions if returnValue is 0
            # If returnValue is not zero, the function will return returnValue
            if returnValue == 0:
                return self.__serverVars.get(server, sr)["top"]
            else:
                return returnValue

        elif section == "hot":

            # Refreshes cache if there is no cache
            try:
                submissions = self.__serverVars.get(server, sr)
                return submissions["hot"]
            except:
                pass

            returnValue = self.RefreshCache(server, sr, "hot")

            # Loads the hot submissions of sr, and returns the submissions if returnValue is 0
            # If returnValue is not zero, the function will return returnValue
            if returnValue == 0:
                return self.__serverVars.get(server, sr)["hot"]
            else:
                return returnValue
        else:
            return -2

    def Remove(self, server, subreddit, section, submission):
        sr = "hentai"

        # Checks to see if the subreddit is valid
        # If the subreddit is not valid, it will be defaulted to r/hentai
        if subreddit in self.subreddits:
            sr = subreddit

        # Checks to make sure a valid section was passed
        # Returns -2 if it wasn't a valid section
        if section == "top":
            # Removes top submission from sr
            # If it fails, -1 is returned
            try:
                submissions = self.__serverVars.get(server, sr)
                submissions["top"].remove(submission)

                self.__serverVars.set(server, sr, submissions)
                self.__serverVars.save(self.serverVarsFp)
            except:
                return -1

        elif section == "hot":
            # Removes hot submission from sr
            # If it fails, -1 is returned
            try:
                submissions = self.__serverVars.get(server, sr)
                submissions["hot"].remove(submission)

                self.__serverVars.set(server, sr, submissions)
                self.__serverVars.save(self.serverVarsFp)
            except:
                return -1
        else:
            return -2

    def getSubmission(self, link):
        return self.__bot.submission(url=link)
