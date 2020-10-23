import time
import schedule
import logging
from dumper import dump_db
from datetime import datetime

def schedule_job(job, day_time):
    """
    Parameters:
        job(function): specifies the function to be executed as a job.
        day_time(str): specifies the time of day on which the job will
                       be executed.
    """
    schedule.every().day.at(day_time).do(job)

    while True:
        schedule.run_pending()
        time.sleep(5)