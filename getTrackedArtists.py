import code
import json
import pycurl
from   StringIO import StringIO
from   argparse import ArgumentParser
from   songkick import *


if __name__ == "__main__":

    parser = ArgumentParser("Find interesting events in metro areas")
    parser.add_argument("user", help="Songkick username")
    args = parser.parse_args()

    buffer = StringIO()

    url = metroSearchUrl.format(args.user, apikey)+"&per_page=all"

    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    metroStr = buffer.getvalue()
    metroJ   = json.loads(metroStr)

    for l in metroJ["resultsPage"]["results"]["location"]:
        m = l["metroArea"]
        print "{} {} {}".format(m["id"],m["displayName"],m["country"]["displayName"])

    #aIDs  = [a["id"] for a in metroJ["resultsPage"]["results"]["artist"]]
    #idMap = {a["id"]: a["displayName"] for a in metroJ["resultsPage"]["results"]["artist"]}

