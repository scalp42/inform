from __future__ import absolute_import

from celery import task

from datetime import timedelta

import requests
from requests import ConnectionError
import json


URL = "http://yarratrams.com.au/base/tramTrackerController/TramInfoAjaxRequest"
PARAMS = {
    'LowFloorOnly': False,
    'Route': 8,
    'StopID': 1568,
}


@task()
def eggsbacon():
#class InformPlugin(InformBasePlugin):
#    def process(self):
    print 'eggsbacon'
    try:
        r = requests.post(URL, data=PARAMS)
    except ConnectionError:
        raise Exception("HTTP Connection failed to %s" % URL)

    trams = json.loads(r.text)
    data = {
        'first': trams['TramTrackerResponse']['ArrivalsPages'][0][0]['Arrival'],
        'second': trams['TramTrackerResponse']['ArrivalsPages'][0][1]['Arrival'],
    }
    return data


