import os

from absl.testing import absltest
import dotenv
import pydantic

from db import client

_DROP_TEST_TABLE = """
DROP TABLE IF EXISTS public.test_table
"""

_CREATE_TEST_TABLE = """
CREATE TABLE public.test_table (
	column1 varchar NULL,
	column2 varchar,
	column3 varchar
);

"""


class DummyObject(pydantic.BaseModel):
    column1: str
    column2: str
    column3: str

    def as_dict(self) -> dict[str, str]:
        return {
            "column1": self.column1,
            "column2": self.column2,
            "column3": self.column3,
        }


class PostgresDBClientTests(absltest.TestCase):
    def setUp(self):
        dotenv.load_dotenv("./riot/.env")

    def test_build_postgres_connection(self):
        db = client.PostgreSQLClient(
            dbname="tftdb",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
        )

        self.assertFalse(db.closed)
        db.close()

    def test_insert(self):
        db = client.PostgreSQLClient(
            dbname="tftdb",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
        )

        _ = db._execute(_DROP_TEST_TABLE)  # pylint: disable=protected-access
        _ = db._execute(_CREATE_TEST_TABLE)  # pylint: disable=protected-access

        data = DummyObject(
            column1="abc",
            column2="def",
            column3="ghi",
        )
        db.insert(
            table_name="test_table",
            attrs=list(data.as_dict().keys()),
            data_to_insert=data.as_dict(),
        )

        c = db._execute(  # pylint: disable=protected-access
            """
           SELECT EXISTS (
               SELECT 1 
               FROM information_schema.tables 
               WHERE table_schema = 'public' 
               AND table_name = 'test_table'
           );
           """
        )
        self.assertTrue(c.fetchone()[0])

        db._execute(_DROP_TEST_TABLE)  # pylint: disable=protected-access
        db.commit()
        db.close()


if __name__ == "__main__":
    absltest.main()
