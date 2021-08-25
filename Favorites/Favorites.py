from discord_variables_plugin import GlobalUserVariables


class Favorites:
    userVarsFp = "users.var"
    __userVars = GlobalUserVariables()

    def __init__(self):
        # Attempts to load self.userVarsFp
        # If that fails, an empty save will be created
        try:
            self.__userVars.load(self.userVarsFp)
        except:
            self.__userVars.save(self.userVarsFp)

    def add(self, user, submission):
        try:
            favorites = self.__userVars.get(user, "favorites")
        except:
            favorites = []

        favorites.append(submission)

        self.__userVars.set(user, "favorites", favorites)
        self.__userVars.save(self.userVarsFp)

    def get(self, user):
        self.__userVars.load(self.userVarsFp)

        try:
            return self.__userVars.get(user, "favorites")
        except:
            return -1

    def remove(self, user, index):
        try:
            favorites = self.__userVars.get(user, "favorites")
        except:
            return -1

        try:
            del favorites[index]
        except:
            return -2

        self.__userVars.set(user, "favorites", favorites)
        self.__userVars.save(self.userVarsFp)

    def clear(self, user):
        try:
            self.__userVars.removeVar(user, "favorites")
        except:
            return -1
