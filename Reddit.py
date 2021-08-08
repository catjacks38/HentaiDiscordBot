import praw
import pickle
import time


class Submissions():
    def __init__(self, time, submissions):
        self.time = time
        self.submissions = submissions


class ImageScrapper:
    topCacheRefreshTime = 600

    def __init__(self, clientID, clientSecret):
        self.__bot = praw.Reddit(user_agent="Image Scrapper Thing (by u/catjacks38)", client_id=clientID, client_secret=clientSecret)
        try:
            with open("top.obj", "rb") as topFile:
                self.__top = topFile.read()
        except:
            self.__top = False

    def GetTop(self):
        topImages = []

        if self.__top:
            submissions = pickle.loads(self.__top)

            if int(time.time()) - submissions.time < self.topCacheRefreshTime:
                return submissions.submissions
            else:
                topImages = []

        try:
            posts = self.__bot.subreddit("hentai").top("day", limit=None)
        except:
            return -1

        for post in posts:
            url = post.url

            if url[:18] == "https://i.redd.it/" or url[:20] == "https://i.imgur.com/":
                topImages.append(url)
        with open("top.obj", "wb") as topFile:
            pickle.dump(Submissions(int(time.time()), topImages), topFile)

        with open("top.obj", "rb") as topFile:
            self.__top = topFile.read()

        return topImages
