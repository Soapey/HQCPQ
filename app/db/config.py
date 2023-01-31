import os
from app.db.SQLiteCursor import SQLiteCursor, PRODUCTION_SQLITE_PATH
from app.db.SQLServerCursor import SQLServerCursor, DATABASE_NAME
from app.db.db_type_enum import DbType


db_type: DbType = None


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
                for tbl_tuple in cur.tables(tableType="TABLE"):
                    if tbl_tuple[1] == "dbo":
                        cur.execute(f"DROP TABLE IF EXISTS {tbl_tuple[2]};")

                with open(r"app\db\sqlserver_init.sql", mode="r") as f:
                    script_contents = f.read()
                    cur.execute(script_contents)
