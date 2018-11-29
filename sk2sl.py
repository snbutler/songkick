#!/usr/bin/env python3

from sys  import stderr
from code import interact
from argparse import ArgumentParser
from songkick import *
from setlist  import *
import pprint
import json

def rev_date(date):
    (d, m, y) = date.split("-")
    return "{}-{}-{}".format(y, m, d)


if __name__ == "__main__":

    parser = ArgumentParser("setlist urls of sk gigs")
    parser.add_argument("user",    help="Songkick username")
    parser.add_argument("sk_keyfile", help="path to file containing songkick apikey")
    parser.add_argument("sl_keyfile", help="path to file containing setlist apikey")
    args = parser.parse_args()

    keys = {}
    with open(args.sk_keyfile) as f:
        keys["songkick"] = f.readline().strip()
    with open(args.sl_keyfile) as f:
        keys["setlist"] = f.readline().strip()

    sk = Songkick(keys["songkick"])
    sl = Setlist(keys["setlist"])

    pp = pprint.PrettyPrinter()

    # gigs = sk.getUserGigs(args.user)
    with open("sk.cache") as cache:
        gigs = json.load(cache)
    # interact(local=locals())

    setlists = []
    for g in gigs:
        pp.pprint(g)
        for p in g["performance"]:
            setlists.append(sl.findGig(artistName=p["artist"]["displayName"], date=rev_date(g["start"]["date"])))
            if len(setlists[-1]) != 1:
                interact(local=locals())

