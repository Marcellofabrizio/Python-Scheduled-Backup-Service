from dumper import dump_db
from scheduler import schedule_job
from file_handler import zipdir
import uploader

def backup_that_shit():
    """
    Main function to execute the dumps, zip and upload to S3
    """

if __name__=="__main__":
    day_time = "10:30" 
    schedule_job(backup_that_shit, day_time)