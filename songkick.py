import requests
from code import interact

class Songkick:

    def __init__(self, apikey):
        self.baseUrl        = "http://api.songkick.com/api/3.0/"
        self.userUrl        = self.baseUrl + "users/{}/artists/tracked.json?apikey={}"
        self.metroUrl       = self.baseUrl + "metro_areas/{}/calendar.json?apikey={}"
        self.metroSearchUrl = self.baseUrl + "search/locations.json?query={}&apikey={}"
        self.artistGigUrl   = self.baseUrl + "artists/{}/gigography.json?apikey={}"
        self.userGigUrl     = self.baseUrl + "users/{}/gigography.json?apikey={}"

        self.user = None
        self._apikey = apikey

        self._req  = requests.session()

    def getUserGigs(self, user = None):
        if not user:
            user = self.user

        results = []

        page = 1
        while True:
            x = self._req.get(self.userGigUrl.format(user, self._apikey)+"&per_page=50&page={}".format(page))
            j = x.json()
            # try:
            if j["resultsPage"]["status"] == "ok" and j["resultsPage"]["results"]:
                results += j["resultsPage"]["results"]["event"]
                page    += 1
            else:
                break
            # except Exception as e:
                # print(e)
                # interact(local=locals())

        return results


