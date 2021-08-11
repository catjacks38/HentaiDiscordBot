import praw
import pickle
import time


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
    hotLimit = 200
    topLimit = 200

    def __init__(self, clientID, clientSecret):
        # Creates bot
        self.__bot = praw.Reddit(user_agent="Image Scrapper Thing (by u/catjacks38)", client_id=clientID, client_secret=clientSecret)

        # Tries to read the cache files--sets them to False if they do not exist or can't be read
        try:
            with open("top.post", "rb") as topFile:
                self.__top = topFile.read()
        except:
            self.__top = False

        try:
            with open("hot.post") as hotFile:
                self.__hot = hotFile.read()
        except:
            self.__hot = False

    def RefreshCache(self, section):
        images = []

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
                images.append(url)

        # Saves the posts and the time to the correct cache file
        if section == "top":
            with open("top.post", "wb") as topFile:
                pickle.dump(Submissions(int(time.time()), images), topFile)

            with open("top.post", "rb") as topFile:
                self.__top = topFile.read()

        elif section == "hot":
            with open("hot.post", "wb") as hotFile:
                pickle.dump(Submissions(int(time.time()), images), hotFile)

            with open("hot.post", "rb") as hotFile:
                self.__hot = hotFile.read()

        return 0

    def Get(self, section):

        # If section is not a valid section, the function returns -2
        if section == "top":
            if self.__top:
                submissions = pickle.loads(self.__top)

                # Checks if the automatic refresh time has not been reached
                # Refreshes cache if it has
                if int(time.time()) - submissions.time < self.topCacheRefreshTime:
                    return submissions.submissions

            returnValue = self.RefreshCache("top")

            # Loads the top Submission object, and returns the submissions variable if returnValue is 0
            # If returnValue is not zero, the function will return returnValue
            if returnValue == 0:
                return pickle.loads(self.__top).submissions
            else:
                return returnValue

        elif section == "hot":
            if self.__hot:
                submissions = pickle.loads(self.__hot)

                # Checks if the automatic refresh time has not been reached
                # Refreshes cache if it has
                if int(time.time()) - submissions.time < self.hotCacheRefreshTime:
                    return submissions.submissions

            returnValue = self.RefreshCache("hot")

            # Loads the hot Submission object, and returns the submissions variable if returnValue is 0
            # If returnValue is not zero, the function will return returnValue
            if returnValue == 0:
                return pickle.loads(self.__hot).submissions
            else:
                return returnValue
        else:
            return -2
