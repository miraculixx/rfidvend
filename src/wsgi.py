#!/usr/bin/env python

import time
import sys
import os
import json
from flask import Flask, Request, Response, request
application = app = Flask('wsgi')

from rfidpos import RFIDPos
from rfid import RFIDTag
from config import rfidpos_config

def init_config():
    global app, rfidpos_config
    app.rp_config = rfidpos_config
    app.rp_pos = None
    app.rp_user = rfidpos_config['VENDHQ_USER']
    app.rp_pass = rfidpos_config['VENDHQ_PASS']
    app.rp_posurl = rfidpos_config['VENDHQ_URL']

@app.before_first_request
def init():
    app.rp_pos = RFIDPos(app.rp_posurl, app.rfid_user , app.rfid_password)

@app.route('/')
def welcome():
    return 'This is RFIDPOS'

@app.route('/cardtrx')
def card_transaction():
    cardid = request.args.get('cardid', '_none_')
    sale = app.rp_pos.create_sale_from_tag(RFIDTag(bytes=cardid))
    if sale != None:
        return 'Created sale %s' % sale.get('id')
    else:
        return 'Card %s not found' % cardid

@app.route('/listcards')
def list_cards():
    return "Cards: %s " % ','.join(app.rp_pos.cus_by_rfid.keys())

@app.route('/env')
def env():
    return os.environ.get("VCAP_SERVICES", "{}")

@app.route('/mongo')
def mongotest():
    from pymongo import Connection
    uri = mongodb_uri()
    conn = Connection(uri)
    coll = conn.db['ts']
    coll.insert(dict(now=int(time.time())))
    last_few = [str(x['now']) for x in coll.find(sort=[("_id", -1)], limit=10)]
    body = "\n".join(last_few)
    return Response(body, content_type="text/plain;charset=UTF-8")

def mongodb_uri():
    local = os.environ.get("MONGODB", None)
    if local:
        return local
    services = json.loads(os.environ.get("VCAP_SERVICES", "{}"))
    if services:
        creds = services['mongodb-1.8'][0]['credentials']
        uri = "mongodb://%s:%s@%s:%d/%s" % (
            creds['username'],
            creds['password'],
            creds['hostname'],
            creds['port'],
            creds['db'])
        print >> sys.stderr, uri
        return uri
    else:
        raise Exception, "No services configured"
    
# setup configuration parameters
init_config()


if __name__ == '__main__':
    app.run(debug=True)
