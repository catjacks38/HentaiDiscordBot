import random
from NHentai.nhentai import NHentai
from discord_variables_plugin import GlobalUserVariables


class NHentaiGrabber:
    __nhentai = NHentai()

    userVarsFp = "users.var"

    # All blacklisted tags to comply with discord community guideline
    # Plus these tags are just kinda cringe anyway
    # MonkaTOS
    bannedTags = ["lolicon", "shotacon", "rape"]

    def __init__(self):
        self.__userVars = GlobalUserVariables()

        # Attempts to load self.userVarsFp
        # If that fails, an empty save will be created
        try:
            self.__userVars.load(self.userVarsFp)
        except:
            self.__userVars.save(self.userVarsFp)

    def set(self, user, required, banned, lang):
        # Attempts to set each tag, unless the tag is None
        if banned:
            self.__userVars.set(user, "banned", banned)

        if required:
            # If the required tag is in bannedTags, return -1
            for tag in required:
                if tag in self.bannedTags:
                    return -1

            self.__userVars.set(user, "required", required)

        if lang:
            self.__userVars.set(user, "language", lang)

        # Saves the changes
        self.__userVars.save(self.userVarsFp)

    def get(self, user):
        # Loads self.userVarsFp
        self.__userVars.load(self.userVarsFp)

        # Tries to get the saved tag(s) of user
        # Sets the tag to None if it isn't saved
        try:
            required = self.__userVars.get(user, "required")
        except:
            required = None

        try:
            banned = self.__userVars.get(user, "banned")
        except:
            banned = None

        try:
            lang = self.__userVars.get(user, "language")
        except:
            lang = None

        # If there is no tag saved, return None for that tag
        return required, banned, lang

    def clear(self, user, var=None):
        try:
            # If var is set, remove var of user
            # Else, clear user
            if var:
                self.__userVars.removeVar(user, var)
            else:
                self.__userVars.clearUser(user)

            self.__userVars.save(self.userVarsFp)
        except:
            return -1

    def query(self, query, required, banned, lang):
        searchQuery = ""

        # Appends each tag to searchQuery, unless if the tag is None
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

        # Appends query to searchQuery
        searchQuery += query

        # Attempts to query Nhentai, and pick a random doujin
        # Returns -1, if it fails
        try:
            pages = self.__nhentai.search(searchQuery, sort="popular").total_pages
            searchPage = self.__nhentai.search(searchQuery, sort="popular", page=1 if pages == 0 else random.randint(1, pages))
        except:
            return -1

        if len(searchPage.doujins) == 0:
            return -2

        # A random doujin is chosen
        doujinThumbnail = random.choice(searchPage.doujins)

        # Attempts to return the cover of the doujin, and the doujin
        # Returns -1, if it fails
        try:
            return doujinThumbnail.cover, self.__nhentai.get_doujin(id=doujinThumbnail.id)
        except:
            return -1
