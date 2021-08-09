import praw
import pickle
import time


class Submissions:
    def __init__(self, time, submissions):
        self.time = time
        self.submissions = submissions


class ImageScrapper:
    topCacheRefreshTime = 600
    hotCacheRefreshTime = 210

    hotLimit = 200
    topLimit = 200

    def __init__(self, clientID, clientSecret):
        self.__bot = praw.Reddit(user_agent="Image Scrapper Thing (by u/catjacks38)", client_id=clientID, client_secret=clientSecret)
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

            if url[:18] == "https://i.redd.it/" or url[:20] == "https://i.imgur.com/":
                images.append(url)

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
        if section == "top":
            if self.__top:
                submissions = pickle.loads(self.__top)

                if int(time.time()) - submissions.time < self.topCacheRefreshTime:
                    return submissions.submissions

            returnValue = self.RefreshCache("top")
            print(self.__top)

            if returnValue == 0:
                return pickle.loads(self.__top).submissions
            else:
                return returnValue

        elif section == "hot":
            if self.__hot:
                submissions = pickle.loads(self.__hot)

                if int(time.time()) - submissions.time < self.hotCacheRefreshTime:
                    return submissions.submissions

            returnValue = self.RefreshCache("hot")

            if returnValue == 0:
                return pickle.loads(self.__hot).submissions
            else:
                return returnValue
        else:
            return -2
