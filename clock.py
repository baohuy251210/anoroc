from apscheduler.schedulers.blocking import BlockingScheduler
import data_rebase
import app

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every one minutes.')
    app.app_rerun()


sched.start()