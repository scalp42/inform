from celery.task import Task

from datetime import datetime, timedelta

from lib.memcache_wrapper import cache

from abc import abstractmethod


class InformBasePlugin(Task):
    run_every = timedelta(minutes=30)

    def __call__(self, *args, **kwargs):
        self.process()
        return ""

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        pass

    def load(self, key):
        return cache.get(key)

    def store(self, key, value):
        print {key[15:]: value}
        cache.set(key[15:], value)

    @abstractmethod
    def process(self):
        pass
