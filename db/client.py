import psycopg

_DB_COMMAND_PROMPT = """
    {command} INTO {table_name} {attrs}
    VALUES {values}
"""


class PostgreSQLClient:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: int):
        self._dbname = dbname
        self._user = user
        self._password = password
        self._host = host
        self._port = port

        self._connection = self._build_postgres_db_connection(
            conninfo=f"postgres://{self._user}:{self._password}@{self._host}:{str(self._port)}/{self._dbname}",
        )

    @property
    def cursor(self):
        return self._connection.cursor()

    def _build_postgres_db_connection(self, conninfo: str) -> psycopg.Connection:
        return psycopg.connect(conninfo=conninfo)

    def _build_attr_string(self, attrs: list[str]) -> str:
        return f"({','.join(attrs)})"

    def _build_value_string(self, attrs: list[str]) -> str:
        values = []
        for attr in attrs:
            values.append(f"%({attr})s")
        return f"({','.join(values)})"

    def _execute(self, command: str, params: dict | None = None) -> psycopg.Cursor:
        try:
            cursor = self.cursor
            cursor.execute(command, params)
            return cursor
        except Exception as e:
            raise e

    def commit(self):
        self._connection.commit()

    def insert(self, table_name: str, attrs: list[str], data_to_insert: dict) -> None:
        _ = self._execute(
            command=_DB_COMMAND_PROMPT.format(
                command="INSERT",
                table_name=table_name,
                attrs=self._build_attr_string(attrs),
                values=self._build_value_string(attrs),
            ),
            params=data_to_insert,
        )

    def close(self):
        self.cursor.close()
        self._connection.close()

    def table_exists(self, table_name: str):
        self._execute(
            command=f"""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = '{table_name}'
            );
            """
        )

    @property
    def closed(self) -> bool:
        return self._connection.closed
