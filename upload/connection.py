import mysql.connector
from mysql.connector import errorcode
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Connection():

    user = None
    password = None
    host = None
    db = None

    conn = None

    def __init__(self, user, password, host, db):

        self.user = user
        self.password = password
        self.host = host
        self.db = db

        try:
            logger.info('Connecting to database.')

            connection = connection = mysql.connector.connect(
                user=self.user, password=self.password, host=self.host, database=self.db,  auth_plugin='mysql_native_password')

            connection.autocommit = False

            self.conn = connection

        except mysql.connector.Error as err:

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger.info(
                    "Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logger.info("Database does not exist")
            else:
                logger.info(err)

    def exec_Query(self, Query_params, params):
        cursor = self.conn.cursor()
        cursor.execute(Query_params, params)

    def exec_query_array(self, Query_params, paramsArray):
        cursor = self.conn.cursor()
        cursor.executemany(Query_params, paramsArray)

    def commit(self):
        self.conn.commit()

    def get_cursor(self):
        return self.conn.cursor()

    def exec_query_simple(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
