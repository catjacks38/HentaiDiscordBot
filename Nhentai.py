import random
from NHentai.nhentai import NHentai
from discord_variables_plugin import GlobalUserVariables


class NhentaiScrapper:
    __nhentai = NHentai()

    userVarsFp = "users.var"

    # All blacklisted tags to comply with discord community guideline
    # Plus these tags are just kinda cringe anyway
    # MonkaTOS
    bannedTags = ["lolicon", "shotacon", "rape"]

    def __init__(self):
        self.__userVars = GlobalUserVariables()

        returnValue = self.__userVars.load(self.userVarsFp)

        if returnValue == -1:
            self.__userVars.save(self.userVarsFp)

    def set(self, user, required, banned, defaultLang):
        if banned:
            self.__userVars.set(user, "banned", banned)

        if required:
            self.__userVars.set(user, "required", required)

        if defaultLang:
            self.__userVars.set(user, "defaultLang", defaultLang)

        self.__userVars.save(self.userVarsFp)

    def get(self, user):
        self.__userVars.load(self.userVarsFp)

        banned = self.__userVars.get(user, "banned")
        required = self.__userVars.get(user, "required")
        defaultLang = self.__userVars.get(user, "defaultLang")

        return required if required != -1 else None, banned if banned != -1 else None, defaultLang if defaultLang != -1 else None

    def query(self, query, required, banned, defaultLang):
        searchQuery = ""

        if required:
            for tag in required:
                searchQuery += f"+{tag} "

        if banned:
            for tag in banned + self.bannedTags:
                searchQuery += f"-{tag} "

        if defaultLang:
            searchQuery += f"+{defaultLang} "

        for tag in self.bannedTags:
            searchQuery += f"-{tag} "

        searchQuery += query

        try:
            pages = self.__nhentai.search(searchQuery, sort="popular").total_pages
            searchPage = self.__nhentai.search(searchQuery, sort="popular", page=random.randint(1, pages))
        except:
            return -1

        doujinThumbnail = random.choice(searchPage.doujins)

        return doujinThumbnail.cover, self.__nhentai.get_doujin(id=doujinThumbnail.id)
