from lib.plugin import InformBasePlugin

from celery.task import task

from datetime import timedelta

import requests
import json


URL = "http://yarratrams.com.au/base/tramTrackerController/TramInfoAjaxRequest"
PARAMS = {
    'LowFloorOnly': False,
    'Route': 8,
    'StopID': 1568,
}


class InformPlugin(InformBasePlugin):
    run_every = timedelta(minutes=1)

    def process(self):
        r = requests.post(URL, data=PARAMS)
        trams = json.loads(r.text)
        data = {
            'first': trams['TramTrackerResponse']['ArrivalsPages'][0][0]['Arrival'],
            'second': trams['TramTrackerResponse']['ArrivalsPages'][0][1]['Arrival'],
        }

        self.store(__name__, data)
