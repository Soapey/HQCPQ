import os
from app.db.SQLiteCursor import SQLiteCursor, PROD_SQLITE_PATH, DEV_SQLITE_PATH
from app.db.SQLServerCursor import SQLServerCursor
from app.db.db_type_enum import DbType
from app.db.build_type_enum import BuildType


build_type: BuildType = None
db_type: DbType = None


def get_cursor_type():

    match db_type:
        case DbType.SQLITE:
            return SQLiteCursor(build_type)

        case DbType.SQL_SERVER:
            return SQLServerCursor(build_type)


def start_empty_db():

    start_db(BuildType.DEVELOPMENT, DbType.SQL_SERVER, clean_start=True)


def start_db(
    start_build_type: BuildType, start_db_type: DbType, clean_start: bool = False
):

    global db_type, build_type

    build_type = start_build_type
    db_type = start_db_type
    cursor_type = get_cursor_type()

    match start_db_type:

        case DbType.SQLITE:

            sqlite_db_path = cursor_type.path

            if clean_start and os.path.exists(sqlite_db_path):
                os.remove(sqlite_db_path)

            with cursor_type as cur:
                with open(r"app\db\sqlite_init.sql", mode="r") as f:
                    script_contents = f.read()
                    cur.executescript(script_contents)

        case DbType.SQL_SERVER:

            with cursor_type as cur:

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
