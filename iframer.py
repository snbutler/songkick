#!/usr/bin/env python3

from   sys      import stderr
from   code     import interact
from   argparse import ArgumentParser
from   flask    import Flask, render_template, url_for, session, g
from   songkick import *
from   setlist  import *
import re
import json
import pprint

def rev_date(date):
    (d, m, y) = date.split("-")
    return "{}-{}-{}".format(y, m, d)

app = Flask(__name__)
app.secret_key = b'_6#yxL"FeQ@z\n\xec]/'

def check_session():
    print("check_session")
    print(session.keys())
    if not "sk" in session:
        print("initialise sk key")
        with open("sk_api") as f:
            session.sk = f.readline().strip()

    if not "sl" in session:
        print("initialise sl key")
        with open("sl_api") as f:
            session.sl = f.readline().strip()

    if not "gigs" in session:
        # gigs = sk.getUserGigs(args.user)
        print("load from cache")
        with open("sk.cache") as cache:
            session["gigs"] = json.load(cache)["songkick"]

    g.sk = Songkick(session.sk)
    g.sl = Setlist(session.sl)
    #interact(local=locals())

@app.route("/user")
@app.route("/user/<username>")
def hello(username=None):
    return render_template('hello.html', name=username)

@app.route("/gig")
@app.route("/gig/<int:n>")
@app.route("/gig/<int:n>/<int:m>")
def gig(n=0, m=0):
    check_session()
    print("checked")

    if n < 0 or n > len(session["gigs"]):
        return render_template('error.html', n=len(session["gigs"]))
    else:
        print("valid n")
        gig = session["gigs"][n]
        if not "gig_n" in session or session["gig_n"] != n:
            print("populating session")
            session["gig_n"]    = n
            session["setlists"] = []
            #interact(local=locals())
            for p in gig["performance"]:
                for s in g.sl.findGig(artistName=p["artist"]["displayName"], date=rev_date(gig["start"]["date"])):
                    session["setlists"].append(s["url"])

        if not "setlists" in session or m < 0 or m > len(session["setlists"]):
            print("invalid m")
            return render_template('error.html', n=len(session["setlists"]))
        else:
            print("rendering")
            #interact(local=locals())

            pp = pprint.PrettyPrinter()

            prev_n = n-1 if n > 0 else None
            next_n = n+1 if n < len(session["gigs"])-1 else None
            prev_m = m-1 if m > 0 else None
            next_m = m+1 if m < len(session["setlists"])-1 else None

            print(session["setlists"][m])

            return render_template('iframer.html', 
                                   #sk_url = re.sub("http:", "https:", re.sub("\?.*", "", gig["uri"])), 
                                   sk_data = pp.pformat(gig),
                                   sl_url  = session["setlists"][m],
                                   n       = n,
                                   m       = m,
                                   max_n   = len(session["gigs"]),
                                   max_m   = len(session["setlists"])
                                  )

with app.test_request_context():
    pass
    #gig(0)
    #interact(local=locals())

    #print(url_for('user', username="simon"))
    #print(url_for('gig', n=0))
    #print(url_for('gig', n=10))
