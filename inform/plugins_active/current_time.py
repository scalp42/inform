from lib.plugin import MonitorBasePlugin

import datetime


class MonitorPlugin(MonitorBasePlugin):
    run_every = datetime.timedelta(minutes=2)
    plugin_name = "current_time"

    def process(self):
        data = datetime.datetime.now().isoformat()

        self.store(data)
        return data
