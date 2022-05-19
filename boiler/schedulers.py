from .job import do_job
from .constants import DELTA_TIME
from apscheduler.schedulers.background import BackgroundScheduler


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(do_job, 'interval', seconds=DELTA_TIME*0.01)
    scheduler.start()
