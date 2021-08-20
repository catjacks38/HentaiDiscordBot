import random
from NHentai.nhentai import NHentai
from discord_variables_plugin import GlobalUserVariables


class NhentaiScrapper:
    __nhentai = NHentai()

    userVarsFp = "users.var"

    # All blacklisted tags to comply with discord community guideline
    # Plus these tags are just kinda cringe anyway
    # MonkaTOS
    bannedTags = ['drugs', 'cheating', 'pregnant', 'netorare', 'mind control', 'lolicon', 'shotacon', 'incest', 'gore', 'vore', 'Scat', 'Rape']

    def __init__(self):
        self.__userVars = GlobalUserVariables()

        returnValue = self.__userVars.load(self.userVarsFp)

        if returnValue == -1:
            self.__userVars.save(self.userVarsFp)

    def set(self, user, required, banned, lang):
        if banned:
            self.__userVars.set(user, "banned", banned)

        if required:
            self.__userVars.set(user, "required", required)

        if lang:
            self.__userVars.set(user, "lang", lang)

        self.__userVars.save(self.userVarsFp)

    def get(self, user):
        self.__userVars.load(self.userVarsFp)

        banned = self.__userVars.get(user, "banned")
        required = self.__userVars.get(user, "required")
        lang = self.__userVars.get(user, "lang")

        return required if required != -1 else None, banned if banned != -1 else None, lang if lang != -1 else None

    def clear(self, user):
        self.__userVars.clearUser(user)
        self.__userVars.save(self.userVarsFp)

    def query(self, query, required, banned, lang):
        searchQuery = ""

        if required:
            for tag in required:
                searchQuery += f"+{tag} "

        if banned:
            for tag in banned + self.bannedTags:
                searchQuery += f"-{tag} "

        if lang:
            searchQuery += f"+{lang} "

        for tag in self.bannedTags:
            searchQuery += f"-{tag} "

        searchQuery += query

        try:
            pages = self.__nhentai.search(searchQuery, sort="popular").total_pages
            searchPage = self.__nhentai.search(searchQuery, sort="popular", page=1 if pages == 0 else random.randint(1, pages))
        except:
            return -1

        doujinThumbnail = random.choice(searchPage.doujins)

        try:
            return doujinThumbnail.cover, self.__nhentai.get_doujin(id=doujinThumbnail.id)
        except:
            return -1
