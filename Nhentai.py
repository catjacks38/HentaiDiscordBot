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
        returnValue = self.__userVars.load(self.userVarsFp)

        if returnValue == -1:
            self.__userVars.save(self.userVarsFp)

    def set(self, user, required, banned, lang):
        # Attempts to set each tag, unless the tag is None
        if banned:
            self.__userVars.set(user, "banned", banned)

        if required:
            # Checks to make sure required is not -1 before iterating
            if required != -1:
                # If the required tag is in bannedTags, return -1
                for tag in required:
                    if tag in self.bannedTags:
                        return -1

            self.__userVars.set(user, "required", required)

        if lang:
            self.__userVars.set(user, "lang", lang)

        # Saves the changes
        self.__userVars.save(self.userVarsFp)

    def get(self, user):
        # Loads self.userVarsFp
        self.__userVars.load(self.userVarsFp)

        # Gets every saved tag of user
        banned = self.__userVars.get(user, "banned")
        required = self.__userVars.get(user, "required")
        lang = self.__userVars.get(user, "lang")

        # If there is no tag saved, return None for that tag
        return required if required != -1 else None, banned if banned != -1 else None, lang if lang != -1 else None

    def clear(self, user):
        # Clears the user's tags, and saves the changes
        self.__userVars.clearUser(user)
        self.__userVars.save(self.userVarsFp)

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
