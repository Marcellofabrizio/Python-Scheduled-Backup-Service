import gzip
import os
from datetime import datetime
from subprocess import Popen
from subprocess import PIPE
from sh import pg_dump

def dump_db(host_name, port, user, database, password):
    """
    Dumps the given Postgresql database 
    
    Args:
        host_name(str): the string which represents the name of the database host.
        port(str): specifies the TCP port or local Unix domain socket file extension 
                   on which the server is listening for connections.
        user(str): user to conect as.
        database(str): specifies the name of the database to connect to.
        password(str): specifies the password of the given database.
    """

    output_file = create_time_stamp(database)

    dump_command = 'pg_dump -h {0} -p {1} -U {2} -w -d {3} > output_files/{4}'\
                    .format(host_name, port, user, database, output_file)

    p = Popen(dump_command, shell=True, env={'PGPASSWORD': password})

    p.wait()

def create_time_stamp(database=None):
    """
    Creates the name of the output file with the given database name and date

    Args:
        database: specifies the database that is being dumped 
    Returns:
        file_name: the .sql file name with the date and time of the backup
    """

    replace_values = {'-': '_', ':': '_', ' ': '_'}

    current_date = str(datetime.now().replace(microsecond=0))

    file_name = (database + '_' + str(current_date) + '.sql')
    return file_name.replace('-', '_').replace(' ', '_').replace(':', '_')
