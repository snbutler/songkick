import code
import json
import pycurl
from   sys      import stderr
from   StringIO import StringIO
from   argparse import ArgumentParser
from   songkick import *


if __name__ == "__main__":

    parser = ArgumentParser("Find interesting events in metro areas")
    parser.add_argument("user", help="Songkick username")
    parser.add_argument("id",   help="ID number of metro area")
    args = parser.parse_args()

    buffer = StringIO()

    url = userUrl.format(args.user, apikey)+"&per_page=all"

    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    userStr = buffer.getvalue()
    userJ   = json.loads(userStr)
    buffer.close()

    aIDs   = [a["id"] for a in userJ["resultsPage"]["results"]["artist"]]
    idMap  = {a["id"]: a["displayName"] for a in userJ["resultsPage"]["results"]["artist"]}

    total  = 0
    events = {}

    page   = 1
    url    = metroUrl.format(args.id, apikey)+"&per_page=50&page={}"
    while True:
        print >> stderr, "Page: {}\r".format(page),

        buffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url.format(page))
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()

        metroStr = buffer.getvalue()
        try:
            metroJ   = json.loads(metroStr)
        except:
            code.interact(local=locals())
        buffer.close()

        if metroJ["resultsPage"]["status"] == "ok" and len(metroJ["resultsPage"]["results"]):
            page += 1
            for e in metroJ["resultsPage"]["results"]["event"]:
                for p in e["performance"]:
                    a = p["artist"]
                    if a["id"] in aIDs:
                        if not e["start"]["date"] in events:
                            events[e["start"]["date"]] = []
                        total += 1
                        events[e["start"]["date"]].append(a["displayName"])

                        print "{} {} @ {}".format(e["start"]["date"], a["displayName"].encode("utf-8"), e["venue"]["displayName"].encode("utf-8"))
                #n = ", ".join([p["displayName"] for p in e["performance"]])
                #code.interact(local=locals())

        else:
            break

    print "Unique: {}; Total: {}".format(len(events), total)
