#!/bin/env python2

import logging
import random
import time
from flask import Flask, g, request

log = logging.getLogger('rolling')
log.info('importing %s...', 'ver_b')

# do busy work to delay starting up
for i in range(10**7 * random.randint(3, 10)):
    i *= 3.71543
    i %= 1000000

# Setup the app
app = Flask(__name__)
ver_name = 'ver_b'

@app.route("/")
def index():
    return "Serving the request from " + ver_name + "\n", 202

@app.route("/fast/")
def fast():
    return "Serving the request from " + ver_name + "\n", 202

@app.route("/slow/")
def slow():
    time.sleep(3 + random.random() * 3)
    return "Serving the request from " + ver_name + "\n", 202

@app.before_request
def before_request():
    """ Run at the beginning of each request """
    g.start_time = time.time()
    log.debug('starting request %s', request.path)

@app.after_request
def after_request(resp):
    """ Runs after ever request """
    total_duration = (time.time() - g.start_time)
    return resp

@app.teardown_request
def teardown_request(err):
    total_duration = (time.time() - g.start_time) * 1000
    log.debug('done request %s, duration %sms', request.path, total_duration)

@app.errorhandler(404)
def page_not_found(error):
    """404 Error Handling function """
    return '404 ' + ver_name + "\n", 404

@app.errorhandler(410)
def page_gone(error):
    """410 Error Handling function """
    return '410 ' + ver_name + "\n", 410

@app.errorhandler(500)
def page_server_error(error):
    """500 Error Handling function """
    return '500 ' + ver_name + "\n", 500

@app.errorhandler(403)
def page_forbidden(error):
    """403 Error Handling function """
    return '403 ' + ver_name + "\n", 403

@app.errorhandler(401)
def page_not_auth(error):
    """401 Error Handling function """
    return '401 ' + ver_name + "\n", 401


if __name__ == "__main__":
    app.run()

