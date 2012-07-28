from __future__ import absolute_import

from celery.task import periodic_task

from inform import modules
from inform.storage import store

from datetime import datetime, timedelta

# initialise plugin run state
run_state = {}
for name in modules.keys():
    run_state[name] = {
        'last_run': None,
        'next_run': datetime.now(),
        'fail_count': 0,
        'last_task_result': None,
    }


@periodic_task(run_every=timedelta(minutes=1))
def scheduler():
    for name in modules.keys():
        if name == "tramtracker":
            # check result of last run
            result = run_state[name]['last_task_result']

            if result is not None and result.successful():
                run_state[name]['fail_count'] = 0
                run_state[name]['next_run'] = datetime.now()
            
            elif result is not None and result.failed():
                run_state[name]['fail_count'] += 1
                run_state[name]['next_run'] = datetime.now() + timedelta(minutes=run_state[name]['fail_count'])

            run_module(name)


def run_module(name):
    print run_state[name]['next_run']

    if datetime.now() >= run_state[name]['next_run']:
        run_state[name]['last_run'] = datetime.now()
        module_task = modules[name].subtask()
        run_state[name]['last_task_result'] = modules[name].delay(link=store.s(name))
    else:
        run_state[name]['last_task_result'] = None


