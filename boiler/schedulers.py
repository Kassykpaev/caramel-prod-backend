from .jobs import update_models
from .constants import MAKING_TIME
from apscheduler.schedulers.background import BackgroundScheduler


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_models, 'interval', seconds=0.2)
    scheduler.start()
