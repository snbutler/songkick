#!/usr/bin/env python3

from   sys      import stderr
from   code     import interact
from   argparse import ArgumentParser
from   flask    import Flask, render_template, url_for, session
from   songkick import *
from   setlist  import *
import json

def rev_date(date):
    (d, m, y) = date.split("-")
    return "{}-{}-{}".format(y, m, d)

app = Flask(__name__)
app.secret_key = b'_6#yxL"FeQ@z\n\xec]/'

def check_session():
    if not "sk" in session:
        keys = {}
        with open("sk_api") as f:
            keys["songkick"] = f.readline().strip()
        with open("sl_api") as f:
            keys["setlist"] = f.readline().strip()

        session["sk"] = Songkick(keys["songkick"])
        session["sl"] = Setlist(keys["setlist"])

        # gigs = sk.getUserGigs(args.user)
        with open("sk.cache") as cache:
            session["gigs"] = json.load(cache)
    #interact(local=locals())

@app.route("/user")
@app.route("/user/<username>")
def hello(username=None):
    return render_template('hello.html', name=username)

@app.route("/gig/<int:n>")
def gig(n=None):
    if n is None or n < 0 or n > abs(session["gigs"]):
        return render_template('error.html', n=abs(session["gigs"]))
    else:
        check_session()

        g = session["gigs"][n]
        print(g)
        setlists = []
        for p in g["performance"]:
            s = session["sl"].findGig(artistName=p["artist"]["displayName"], date=rev_date(g["start"]["date"]))
        #interact(local=locals())
        return render_template('iframer.html', sk_url=sk_url, setlists=setlists)

with app.test_request_context():
    pass
    #gig(0)
    #interact(local=locals())

    #print(url_for('user', username="simon"))
    #print(url_for('gig', n=0))
    #print(url_for('gig', n=10))
