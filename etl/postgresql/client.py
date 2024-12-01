from loguru import logger
import psycopg
from psycopg.errors import Error

from etl.postgresql import settings


class PostgresDB:
    _tft_db_name = "tftdb"

    def __init__(self):
        self._settings = settings.load_settings()
        self._host = self._settings.host
        self._port = self._settings.port
        self._user = self._settings.user
        self._password = self._settings.password
        self._connect()

    def _connect(self):
        try:
            self.conn = psycopg.connect(
                host=self._host, port=self._port, dbname=self._tft_db_name, user=self._user, password=self._password
            )
            self.cursor = self.conn.cursor()
            logger.info("Connection Success")
        except Error as e:
            logger.error(f"Connection failed with error {e}")
            raise

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logger.info("Connection Closed")

    def _execute_query(self, query: str, params: tuple[str, ...] | None = None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
        except Error as e:
            logger.error(f"Query execution failed with error {e}")
            self.conn.rollback()

    def fetch_all(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            logger.error(f"Query execution failed with error {e}")
            return []

    def insert(self, table: str, data: dict[str, str]):
        columns = data.keys()
        values = tuple(data.values())
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"
        self._execute_query(query, values)

    def update(self, table: str, data: dict[str, str], condition: dict[str, str]):
        set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
        where_clause = " AND ".join([f"{key} = %s" for key in condition.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        values = tuple(data.values()) + tuple(condition.values())
        self._execute_query(query, values)

    def delete(self, table: str, condition: dict[str, str]):
        where_clause = " AND ".join([f"{key} = %s" for key in condition.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        self._execute_query(query, tuple(condition.values()))
