from NHentai.nhentai import NHentai


class NhentaiScrapper:
    nhentai = NHentai()

    # All blacklisted tags to comply with discord community guideline
    # Plus these tags are just kinda cringe anyway
    tagBlacklist = ["lolicon", "shotacon", "rape"]

    def getRandom(self):
        randomDoujin = None
        hasBlacklistedTag = True

        while hasBlacklistedTag:
            randomDoujin = self.nhentai.get_random()

            for tag in randomDoujin.tags:
                hasBlacklistedTag = False

                if tag in self.tagBlacklist:
                    hasBlacklistedTag = True
                    break

        return randomDoujin
