import os
from app.db.SQLiteCursor import SQLiteCursor, PRODUCTION_SQLITE_PATH
from app.db.SQLServerCursor import SQLServerCursor
from app.db.db_type_enum import DbType


db_type: DbType = None


def get_cursor_type():

    match db_type:
        case DbType.SQLITE:
            return SQLiteCursor

        case DbType.SQL_SERVER:
            return SQLServerCursor


def start_empty_sql_server_db():

    start_db(DbType.SQL_SERVER, clean_start=True)


def start_db(start_db_type: DbType, clean_start: bool = False):

    global db_type
    db_type = start_db_type

    match start_db_type:

        case DbType.SQLITE:

            if clean_start and os.path.exists(PRODUCTION_SQLITE_PATH):
                os.remove(PRODUCTION_SQLITE_PATH)

            with SQLiteCursor() as cur:
                with open(r"app\db\sqlite_init.sql", mode="r") as f:
                    script_contents = f.read()
                    cur.executescript(script_contents)

        case DbType.SQL_SERVER:

            with SQLServerCursor() as cur:

                if clean_start:

                    priority_tables = ["dbo.product_rate", "dbo.quote_item"]

                    for tbl_name in priority_tables:
                        cur.execute(
                            f"IF OBJECT_ID('{tbl_name}') IS NOT NULL DROP TABLE {tbl_name};"
                        )

                    for tbl in cur.tables(tableType="TABLE").fetchall():
                        tbl_type = tbl[1]
                        tbl_name = tbl[2]
                        if tbl_type == "dbo" and tbl_name not in priority_tables:
                            cur.execute(
                                f"IF OBJECT_ID('{tbl_name}') IS NOT NULL DROP TABLE {tbl_name};"
                            )

                    with open(r"app\db\sqlserver_init.sql", mode="r") as f:
                        script_contents = f.read()
                        cur.execute(script_contents)
