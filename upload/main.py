# from upload.Log import Log
import connection as conn
from log import Log
import json
import csv
import logging
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

log: None


def main(file_name):
    global log

    connection = get_connection()
    log = Log(connection)

    log.new_log(file_name, 'N/A', 'Starting process', 0)
    create_table(connection)

    insert_data(file_name, connection)

    logger.info(f'Upload process finished.')


def get_connection():

    with open('../config.json', 'r') as file:
        config = json.load(file)

    return conn.Connection(user=config['user'], password=config['password'], host=config['host'], db=config['database'])


def create_table(connection):
    logger.info(f'Creating table top_scorers table')
    cursor = connection.get_cursor()
    sql_statement = '''
    CREATE TABLE IF NOT EXISTS top_scorers (
        name varchar(150),
        minutes_played INT,
        J1 INT,
        J2 INT,
        J3 INT,
        J4 INT,
        J5 INT,
        J6 INT,
        J7 INT,
        J8 INT,
        J9 INT,
        J10 INT,
        J11 INT,
        J12 INT,
        J13 INT,
        J14 INT,
        J15 INT,
        J16 INT,
        J17 INT,
        total_scores INT,
        scores_per_match double,
        scores_every double)
    '''
    cursor.execute(sql_statement)


def insert_data(file_name, connection):
    logger.info(f'Reading data from {file_name}')
    log.new_log(file_name, 'N/A', 'Reading data', 0)
    with open(file_name, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        data = ''
        row_line = 0
        for row in csv_reader:
            if row_line == 0:
                row_line += 1
                continue
            logger.info(f'Reading data {row_line}')

            data += f'''
            ("{row[0]}",
            {row[1]}, {row[2]}, {row[3]},
            {row[4]}, {row[5]}, {row[6]},
            {row[7]}, {row[8]}, {row[9]},
            {row[10]}, {row[11]}, {row[12]},
            {row[13]}, {row[14]}, {row[15]},
            {row[16]}, {row[17]}, {row[18]},
            {row[19]}, {row[20]}, {row[21]}),'''

            log.new_log(file_name, row[0], 'upload', row_line)
            row_line += 1
        data = data[:-1]
        sql_statement = f'INSERT INTO top_scorers VALUES {data}'

        cursor = connection.get_cursor()
        cursor.execute(sql_statement)

        connection.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name',
                        help='Path old file',
                        type=str)

    args = parser.parse_args()
    main(args.file_name)
