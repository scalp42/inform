from celery import Task

from datetime import datetime, timedelta

from lib.memcache_wrapper import cache

from abc import abstractmethod


class InformBasePlugin(Task):
    abstract = True

    def __call__(self, *args, **kwargs):
        self.process()
        return ""

    def on_failure(self, retval, task_id, args, kwargs, einfo):
        print 'EGGGGGGG failure'

    def on_success(self, retval, task_id, args, kwargs):
        print 'EGGGGGGG success'

    def load(self, key):
        return cache.get(key)

    def store(self, key, value):
        print {key[15:]: value}
        cache.set(key[15:], value)

    @abstractmethod
    def process(self):
        pass


class InformBasePlugin2(Task):
    abstract = True

    def __call__(self, *args, **kwargs):
        print '__call__'
        return self.run(*args, **kwargs)


