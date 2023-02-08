from hqcpq.db.SQLServerCursor import SQLServerCursor
from hqcpq.db.build_type_enum import BuildType


build_type: BuildType = None


def get_cursor_type():
    return SQLServerCursor(build_type)


def start_empty_db():
    start_db(BuildType.DEVELOPMENT, clean_start=True)


def start_db(start_build_type: BuildType, clean_start: bool = False):

    global build_type

    build_type = start_build_type
    cursor_type = get_cursor_type()

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

            with open(r"hqcpq\db\sqlserver_init.sql", mode="r") as f:
                script_contents = f.read()
                cur.execute(script_contents)
