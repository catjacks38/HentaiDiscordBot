import praw
import discord_variables_plugin


# A class for scrapping the images off of r/hentai
class ImageScrapper:
    # The limit on how many posts to grab
    topLimit = 200
    hotLimit = 200

    # Server variables file path
    serverVarsFp = "server.vars"

    subreddits = ["hentai", "ecchi"]

    def __init__(self, clientID, clientSecret):
        # Creates bot
        self.__bot = praw.Reddit(user_agent="Image Scrapper Thing (by u/catjacks38)", client_id=clientID, client_secret=clientSecret)
        self.__serverVars = discord_variables_plugin.ServerVariables()

        # Tries to read the cache files--sets them to False if they do not exist or can't be read
        returnValue = self.__serverVars.load(self.serverVarsFp)

        if returnValue == -1:
            self.__serverVars.save(self.serverVarsFp)

    def RefreshCache(self, server, subreddit, section):
        print("refreshing")
        
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

        for post in posts:
            url = post.url

            # Only appends the URL if it is an image URL
            if url[:18] == "https://i.redd.it/" or url[:20] == "https://i.imgur.com/":
                submissions.append(post)

        # Saves the posts to serverVars
        self.__serverVars.set(server, sr, {section : submissions})
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
            submissions = self.__serverVars.get(server, sr)

            # Refreshes cache if there is no cache
            if submissions != -1:
                try:
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
            submissions = self.__serverVars.get(server, sr)

            # Refreshes cache if there is no cache
            if submissions != -1:
                try:
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
