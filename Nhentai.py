import random
from NHentai.nhentai import NHentai


class NhentaiScrapper:
    __nhentai = NHentai()

    # All blacklisted tags to comply with discord community guideline
    # Plus these tags are just kinda cringe anyway
    # MonkaTOS
    bannedTags = ["lolicon", "shotacon", "rape"]

    def getRandom(self):
        randomDoujin = None
        hasBlacklistedTag = True

        while hasBlacklistedTag:
            randomDoujin = self.__nhentai.get_random()

            for tag in randomDoujin.tags:
                hasBlacklistedTag = False

                if tag in self.bannedTags:
                    hasBlacklistedTag = True
                    break

        return randomDoujin

    def query(self, query, banned, required):
        searchQuery = ""

        for tag in banned + self.bannedTags:
            query += f"-{tag} "

        for tag in required:
            query += f"+{tag} "

        searchQuery += query

        pages = self.__nhentai.search(searchQuery, sort="popular").total_pages
        searchPage = self.__nhentai.search(searchQuery, sort="popular", page=random.randint(1, pages))

        doujinThumbnail = random.choice(searchPage.doujins)

        return doujinThumbnail.cover, self.__nhentai.get_doujin(id=doujinThumbnail.id)
