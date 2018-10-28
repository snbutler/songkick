import requests
from code import interact

class Setlist:

    def __init__(self, apikey):
        self.baseUrl = "https://api.setlist.fm/rest/1.0/"
        self.gigUrl  = self.baseUrl + "search/setlists"

        self._apikey = apikey

        self._req  = requests.session()
        self._req.headers["Accept"] = "application/json"
        self._req.headers["x-api-key"] = apikey

    def findGig(self, **kwargs):
        url = self.gigUrl+"?"

        for kw,arg in kwargs:
            url += "{}={}&".format(kw, arg)
        if url[-1] == "&":
            url = url[-1]

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


