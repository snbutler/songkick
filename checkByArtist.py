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
    #parser.add_argument("id",   help="ID number of metro area")
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

    aIDs    = [a["id"] for a in userJ["resultsPage"]["results"]["artist"]]
    idMap   = {a["id"]: a["displayName"] for a in userJ["resultsPage"]["results"]["artist"]}
            
    total   = 0
    events  = {}
    areaIDs = {}

    for a in aIDs[:1]:
        page = 1
        url  = artistGigUrl.format(a, apikey)+"&order=desc&per_page=50&page={}"
        while True:
            print >> stderr, "aID: {}; Page: {}\r".format(a, page),

            buffer = StringIO()
            c = pycurl.Curl()
            c.setopt(c.URL, url.format(page))
            c.setopt(c.WRITEDATA, buffer)
            c.perform()
            c.close()

            gigStr = buffer.getvalue()
            try:
                gigJ   = json.loads(gigStr)
            except:
                code.interact(local=locals())
            buffer.close()

            if gigJ["resultsPage"]["status"] == "ok" and len(gigJ["resultsPage"]["results"]):
                page += 1
                for e in gigJ["resultsPage"]["results"]["event"]:
                    arID = e["venue"]["metroArea"]["id"] 
                    if not arID in areaIDs:
                        areaIDs[arID] = e["venue"]["metroArea"]["displayName"]

                    for p in e["performance"]:
                        a = p["artist"]
                        if not e["start"]["date"] in events[arID]:
                            events[arID][e["start"]["date"]] = []
                        events[arID][e["start"]["date"]].append(a["id"])
            else:
                break

    code.interact(local=locals())
