
import time
import logging
from edu.lagcc.opencc.utils.util import JOB_LOG_NAME
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


@scheduler.scheduled_job('interval', minutes=1)
def search_scheduler():
    logging.getLogger(JOB_LOG_NAME).debug("job started")
    time.sleep(5)
    logging.getLogger(JOB_LOG_NAME).debug("job ended")


scheduler.start()
