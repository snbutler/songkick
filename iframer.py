#!/usr/bin/env python3

from   sys      import stderr
from   code     import interact
from   argparse import ArgumentParser
from   flask    import Flask, render_template, url_for, session, g
from   werkzeug.contrib.cache import SimpleCache
from   songkick import *
from   setlist  import *
import json
import pprint

app = Flask(__name__)
app.secret_key = b'_6#yxL"FeQ@z\n\xec]/'
cache = SimpleCache()

def rev_date(date):
    (d, m, y) = date.split("-")
    return "{}-{}-{}".format(y, m, d)
def check_session():
    print("check_session")
    print(session.keys())

    if not "sk" in session:
        print("initialise sk key")
        with open("sk_api") as f:
            session["sk"] = f.readline().strip()

    if not "sl" in session:
        print("initialise sl key")
        with open("sl_api") as f:
            session["sl"] = f.readline().strip()

    g.sk = Songkick(session["sk"])
    g.sl = Setlist(session["sl"])

    #interact(local=locals())
def get_gigs():
    print("has: ", cache.has("gigs"))
    gigs = cache.get("gigs")
    if not gigs:
        print("load from disk cache")
        # sk = g.sk.getUserGigs(args.user)
        with open("sk.cache") as sk_cache:
            gigs = json.load(sk_cache)["songkick"]
            cache.set("gigs", gigs, timeout=0)
            print("has: ", cache.has("gigs"))
    else:
        print("found mem cache")

    return gigs

@app.route("/user")
@app.route("/user/<username>")
def hello(username=None):
    return render_template('hello.html', name=username)

@app.route("/gig")
@app.route("/gig/<int:n>")
def gig(n=0):
    check_session()
    print("checked")

    gigs = get_gigs()

    if not gigs:
        return render_template('error.html')
    elif n < 0 or n > len(gigs):
        return render_template('error.html', n=len(gigs))
    else:
        print("valid n")
        if not "gig_n" in session or session["gig_n"] != n:
            print("finding setlists")
            #pp = pprint.PrettyPrinter()
            session["gig_n"]    = n
            session["setlists"] = {}
            for p in gigs[n]["performance"]:
                sk_name = p["artist"]["displayName"]
                if not sk_name in session["setlists"]:
                    session["setlists"][sk_name] = []
                for s in g.sl.findGig(artistName=sk_name, date=rev_date(gigs[n]["start"]["date"])):
                    #interact(local=locals())
                    session["setlists"][sk_name].append({"sl_name": s["artist"]["name"],
                                                         "sl_url":  s["url"]})
                if not session["setlists"][sk_name]:
                    session["setlists"][sk_name].append({"sl_name": "create",
                                                         "sl_url":  "https://www.setlist.fm/edit"})

        print("rendering")
        sk_data = {"details":  [gigs[n]["displayName"],
                                gigs[n]["start"]["date"],
                                gigs[n]["end"]["date"] if "end" in gigs[n] else None,
                                gigs[n]["venue"]["displayName"],
                                gigs[n]["location"]["city"],
                                gigs[n]["type"]
                               ],
                   "setlists": session["setlists"]
                  }

        # interact(local=locals())
        arb = next(iter((session["setlists"]).keys()))
        sl_url = session["setlists"][arb][0]["sl_url"] if session["setlists"] else "https://www.setlist.fm/edit"

        return render_template("iframer.html", 
                               sk_data = sk_data,
                               sl_url  = sl_url,
                               n       = n,
                               max_n   = len(gigs),
                              )


with app.test_request_context():
    pass
    #gig(0)
    #interact(local=locals())

    #print(url_for('user', username="simon"))
    #print(url_for('gig', n=0))
    #print(url_for('gig', n=10))
