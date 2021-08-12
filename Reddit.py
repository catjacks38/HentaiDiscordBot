import praw
import discord_variables_plugin


# A class for scrapping the images off of r/hentai
class ImageScrapper:
    # The limit on how many posts to grab
    topLimit = 200
    hotLimit = 200

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

        # Saves the posts to serverVars
        self.__serverVars.set(server, section, submissions)
        self.__serverVars.save(self.serverVarsFp)

        return 0

    def Get(self, section, server):

        # If section is not a valid section, the function returns -2
        if section == "top":
            submissions = self.__serverVars.get(server, "top")

            # Refreshes cache if there is no cache
            if submissions != -1:
                return submissions

            returnValue = self.RefreshCache("top", server)

            # Loads the top submissions, and returns the submissions variable if returnValue is 0
            # If returnValue is not zero, the function will return returnValue
            if returnValue == 0:
                return self.__serverVars.get(server, "top")
            else:
                return returnValue

        elif section == "hot":
            submissions = self.__serverVars.get(server, "hot")

            # Refreshes cache if there is no cache
            if submissions != -1:
                return submissions

            returnValue = self.RefreshCache("hot", server)

            # Loads the hot submissions, and returns the submissions variable if returnValue is 0
            # If returnValue is not zero, the function will return returnValue
            if returnValue == 0:
                return self.__serverVars.get(server, "hot")
            else:
                return returnValue
        else:
            return -2

    def Remove(self, server, section, submission):
        if section == "top":
            try:
                submissions = self.__serverVars.get(server, "top")
                submissions.remove(submission)

                self.__serverVars.set(server, "top", submissions)
                self.__serverVars.save(self.serverVarsFp)
            except:
                return -1
        elif section == "hot":
            try:
                submissions = self.__serverVars.get(server, "hot")
                submissions.remove(submission)

                self.__serverVars.set(server, "hot", submissions)
                self.__serverVars.save(self.serverVarsFp)
            except:
                return -1
        else:
            return -2
