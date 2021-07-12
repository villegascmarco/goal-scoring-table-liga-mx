from datetime import datetime


class Log():
    connection = None

    def __init__(self, connection) -> None:
        self.connection = connection
        self.id = self.__get_id()
        self.__create_table()

    def __get_id(self):
        return datetime.now().strftime("%Y%m%d%H%M%S")

    def __create_table(self):
        cursor = self.connection.get_cursor()

        sql_statement = '''
        CREATE TABLE IF NOT EXISTS upload_log (
            id_process bigint(20),
            archive_name varchar(50),
            player_name varchar(100),
            process varchar(100),
            row_count int(11));'''

        cursor.execute(sql_statement)

    def __create_log(self, archive_name, data, process,  row):
        cursor = self.connection.get_cursor()

        sql_statement = f'''
        INSERT INTO upload_log VALUES ({self.__get_id()},"{archive_name}", "{data}", "{process}", {row});'''

        cursor.execute(sql_statement)
        self.connection.commit()

    def new_log(self, archive_name, data, process, row):
        self.__create_log(archive_name, data, process, row)
