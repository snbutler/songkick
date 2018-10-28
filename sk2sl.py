#!/usr/bin/env python3

from code import interact
from argparse import ArgumentParser
from songkick import *
import pprint


if __name__ == "__main__":

    parser = ArgumentParser("setlist urls of sk gigs")
    parser.add_argument("user",    help="Songkick username")
    parser.add_argument("keyfile", help="path to file containing apikey")
    args = parser.parse_args()

    apikey = None
    with open(args.keyfile) as f:
        apikey = f.readline().strip()

    sk = Songkick(apikey)

    pp = pprint.PrettyPrinter()

    gigs = sk.getUserGigs(args.user)
    interact(local=locals())

