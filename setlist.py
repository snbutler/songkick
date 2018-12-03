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

        for kw,arg in kwargs.items():
            url += "{}={}&".format(kw, arg)
        if url[-1] == "&":
            url = url[:-1]
        #print(url)

        results = []

        page = 1
        done = False
        while not done:
            x = self._req.get(url+"&per_page=50&page={}".format(page))
            if not x:
                break
            j = x.json()

            results += j["setlist"]
            done     = len(results) == j["total"]
            page    += 1
            # interact(local=locals())
            # try:
            # except Exception as e:
                # print(e)
                # interact(local=locals())

        return results


