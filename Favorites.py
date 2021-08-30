from discord_variables_plugin import GlobalUserVariables


# Class for storing submission data to make getting favorite submissions faster
class SubmissionData:
    def __init__(self, imageUrl, shortlink, title, authorName, authorIconUrl):
        self.imageUrl = imageUrl
        self.shortlink = shortlink
        self.title = title
        self.authorName = authorName
        self.authorIconUrl = authorIconUrl


# A class for managing favorites of users
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
        # Attempts to read the user's favorites
        # If it fails, set favorites to an empty list
        try:
            favorites = self.__userVars.get(user, "favorites")
        except:
            favorites = []

        submissionShortLink = submission.shortlink

        # If submission is already in favorites, return -1
        for submissionData in favorites:
            if submissionData.shortlink == submissionShortLink:
                return -1

        # Appends the submission to favorites
        favorites.append(SubmissionData(submission.url, submissionShortLink, submission.title, submission.author.name, submission.author.icon_img))

        # Sets and saved favorites to the favorites variable of user
        self.__userVars.set(user, "favorites", favorites)
        self.__userVars.save(self.userVarsFp)

    def get(self, user):
        # Loads the self.userVarsFp file
        self.__userVars.load(self.userVarsFp)

        try:
            # Tries to get the favorites of user
            favorites = self.__userVars.get(user, "favorites")

            # If favorites of user is empty, clear user's favorites, and return -1
            if not favorites:
                self.clear(user)
                return -1

            return favorites
        except:
            # If there are not favorites of user, return -1
            return -1

    def remove(self, user, index):
        # Tried to get favorites of user
        try:
            favorites = self.get(user)
        except:
            # Returns -1 if there are no saved favorites
            return -1

        # Tries to delete submission of favorites of user at index of index
        try:
            del favorites[index]
        except:
            # Returns -2 if the index doesn't exist
            return -2

        # Sets and saved the favorites of user
        self.__userVars.set(user, "favorites", favorites)
        self.__userVars.save(self.userVarsFp)

    def clear(self, user):
        try:
            # Tries to remove the favorites variable of user, and saved the new file
            self.__userVars.removeVar(user, "favorites")
            self.__userVars.save(self.userVarsFp)
        except:
            # If the user has no favorites, return -1
            return -1
