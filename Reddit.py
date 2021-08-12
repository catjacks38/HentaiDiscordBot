import praw
import time
import discord_variables_plugin


# A class to store the time and a list image urls for the caches, because storing it all in a list caused an error. T_T
class Submissions:
    def __init__(self, time, submissions):
        self.time = time
        self.submissions = submissions


# A class for scrapping the images off of r/hentai
class ImageScrapper:
    # How long until automatic cache refresh (stored in seconds)
    topCacheRefreshTime = 600
    hotCacheRefreshTime = 210

    # The limit on how many posts to grab
    hotLimit = 300
    topLimit = 300

    # Server variables file path
    serverVarsFp = "server.vars"

    def __init__(self, clientID, clientSecret):
        # Creates bot
        self.__bot = praw.Reddit(user_agent="Image Scrapper Thing (by u/catjacks38)", client_id=clientID, client_secret=clientSecret)
        self.__serverVars = discord_variables_plugin.ServerVariables()

        # Tries to read the cache files--sets them to False if they do not exist or can't be read
        returnValue = self.__serverVars.load(self.serverVarsFp)

        if returnValue == -1:
            self.__serverVars.save(self.serverVarsFp)

    def RefreshCache(self, section, server):
        submissions = []

        # Tries to get the submissions, and returns -1 if it fails
        # If section is not a valid section, the function returns -2
        try:
            if section == "top":
                posts = self.__bot.subreddit("hentai").top("day", limit=self.topLimit)
            elif section == "hot":
                posts = self.__bot.subreddit("hentai").hot(limit=self.hotLimit)
            else:
                return -2
        except:
            return -1

        for post in posts:
            url = post.url

            # Only appends the URL if it is an image URL
            if url[:18] == "https://i.redd.it/" or url[:20] == "https://i.imgur.com/":
                submissions.append(post)

        # Saves the posts and the time to serverVars
        self.__serverVars.set(server, section, Submissions(int(time.time()), submissions))
        self.__serverVars.save(self.serverVarsFp)

        return 0

    def Get(self, section, server):

        # If section is not a valid section, the function returns -2
        if section == "top":
            submissions = self.__serverVars.get(server, "top")

            # Checks if the automatic refresh time has not been reached
            # Refreshes cache if it has
            if submissions != -1:
                if int(time.time()) - submissions.time < self.topCacheRefreshTime:
                    return submissions.submissions

            returnValue = self.RefreshCache("top", server)

            # Loads the top Submission object, and returns the submissions variable if returnValue is 0
            # If returnValue is not zero, the function will return returnValue
            if returnValue == 0:
                return self.__serverVars.get(server, "top").submissions
            else:
                return returnValue

        elif section == "hot":
            submissions = self.__serverVars.get(server, "hot")

            # Checks if the automatic refresh time has not been reached
            # Refreshes cache if it has
            if submissions != -1:
                if int(time.time()) - submissions.time < self.hotCacheRefreshTime:
                    return submissions.submissions

            returnValue = self.RefreshCache("hot", server)

            # Loads the hot Submission object, and returns the submissions variable if returnValue is 0
            # If returnValue is not zero, the function will return returnValue
            if returnValue == 0:
                return self.__serverVars.get(server, "hot").submissions
            else:
                return returnValue
        else:
            return -2
