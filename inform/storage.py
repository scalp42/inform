from __future__ import absolute_import

from celery import task

import memcache


class Storage():
    def __init__(self):
        self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)

    def load(self, key):
        return self.mc.get(key)

    def store(self, key, value):
        return self.mc.set(key, value)

storage = Storage()


@task()
def store(module_name):
    print 'storage!'
    print module_name
    #storage.store(module_name, value)
