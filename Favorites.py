from discord_variables_plugin import GlobalUserVariables


# Class for storing submission data
class SubmissionData:
    def __init__(self, imageUrl, shortlink, title, authorName, authorIconUrl):
        self.imageUrl = imageUrl
        self.shortlink = shortlink
        self.title = title
        self.authorName = authorName
        self.authorIconUrl = authorIconUrl


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

        submissionShortLink = submission.shortlink

        for submissionData in favorites:
            if submissionData.shortlink == submissionShortLink:
                return -1

        favorites.append(SubmissionData(submission.url, submissionShortLink, submission.title, submission.author.name, submission.author.icon_img))

        self.__userVars.set(user, "favorites", favorites)
        self.__userVars.save(self.userVarsFp)

    def get(self, user):
        self.__userVars.load(self.userVarsFp)

        try:
            favorites = self.__userVars.get(user, "favorites")

            if not favorites:
                self.clear(user)
                return -1

            return favorites
        except:
            return -1

    def remove(self, user, index):
        try:
            favorites = self.get(user)
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
            self.__userVars.save(self.userVarsFp)
        except:
            return -1
