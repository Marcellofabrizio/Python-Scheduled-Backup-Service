import os
import zipfile
import shutil
import fnmatch
import logging
from datetime import datetime


def zipdir(dump_path, zip_path, database=None, all_files=False, remove_dumps=True):
    """
    Zips all files from directory from given database  

    Args:
        dump_path: the path to the dump files.
        zip_path: the path to the zip directory.
        database: specifies the dumps which should be zipped. If None,
                  all dumps will be zipped.
        remove_dumps: if True, will remove the remaining dumps after
                      they are zipped. Only recommend setting it False
                      for testing reasons.
    """
    if all_files == True and database == None:
        file_pattern = '*.sql' #will zip any .sql file 
        database = 'backup_all'

    elif all_files == True and database != None:
        logging.error('Cannot have both all files and a defined database, dummy')
        return

    else:
        file_pattern = database + '_*.sql'

    
    zip_file_name = create_time_stamp(zip_path + '/' + database)
    zipf = zipfile.ZipFile( zip_file_name, 'w', zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk(dump_path):
        for file in fnmatch.filter(files, file_pattern):
            zipf.write(os.path.join(root, file))

    if len(zipf.filelist) == 0:
        remove_file(zipf.filename)

    zipf.close()
    remove_files(dump_path, file_pattern)
    return zip_file_name

def create_time_stamp(file_name):

    current_date = str(datetime.now().replace(microsecond=0))

    time_stamp = (file_name + '_' + str(current_date) + '.zip')
    return time_stamp.replace('-', '_').replace(' ', '_').replace(':', '_')

def remove_files(path, file_pattern):
    """
    Removes unzipped files from the backup_files

    Args:
        path: path to the directory.
        file_pattern: specifies which files will be deleted based on a pattern.
    """
    
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, file_pattern):
            try:
                os.remove(os.path.join(root, file))
            except OSError as e:
                logging.error(e)

def remove_file(file_path):
    try:
        os.remove(file_path)
    except OSError as e:
        logging.error(e)
    
def move_file(file):
    os.rename(file, 'zip_files' + '/' + file)

zipdir('dump_files', 'backup_files', 'master')