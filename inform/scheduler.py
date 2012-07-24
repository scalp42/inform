from __future__ import absolute_import

from celery.task import periodic_task
from celery.result import AsyncResult

from inform import modules

from datetime import datetime, timedelta

# initialise plugin run state
run_state = {}
for name in modules.keys():
    run_state[name] = {
        'last_run': None,
        'success_count': 0,
        'fail_count': 0,
        'last_task_result': None,
    }


@periodic_task(run_every=timedelta(minutes=1))
def scheduler():
    for name in modules.keys():
        if name == "tramtracker":
            # check result of last run
            result = run_state[name]['last_task_result']
            if result is None:
                run(name)
            elif result.successful():
                run_state[name]['success_count'] += 1
                run_state[name]['fail_count'] = 0
                run(name)
            elif result.failed():
                run_state[name]['fail_count'] += 1
                run_state[name]['success_count'] = 0
                run(name)

            # if now() > fail_count * mins since last_run

            print run_state[name]['last_task_result']

    # record last run time and task_id
    # on next run, check the result and decide to run again or not..
    # range between every 1 min, to every 1 hour

def run(module_name):
    run_state[module_name]['last_run'] = datetime.now()
    run_state[module_name]['last_task_result'] = modules[module_name].delay()


