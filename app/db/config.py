from app.db.SQLCursor import SQLCursor, PRODUCTION_SQLITE_PATH
import sys
import os


def start_db(clean_start: bool = False):

    if clean_start and os.path.exists(PRODUCTION_SQLITE_PATH):
        os.remove(PRODUCTION_SQLITE_PATH)
        
    with SQLCursor() as cur:
        with open(r'app\db\init.sql', mode='r') as f:
            script_contents = f.read()
            cur.executescript(script_contents)


if __name__ == '__main__':

    build_name = sys.argv[1]

    start_db(build_name, True)