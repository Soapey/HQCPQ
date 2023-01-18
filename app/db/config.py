import sys
import os
from db.SQLCursor import SQLCursor


TEST_SQLITE_PATH = r'db\hqcpq-test.sqlite3'
PRODUCTION_SQLITE_PATH = r'db\hqcpq.sqlite3'


builds = {
    'test': TEST_SQLITE_PATH,
    'production': PRODUCTION_SQLITE_PATH
}


def start(build_name: str, clean_start: bool = False):

    if build_name not in builds.keys():
        print(f'build name: {build_name} not recognised.')
        return
    
    path = builds[build_name]

    if clean_start and os.path.exists(path):
        os.remove(path)
        
    print(f'starting with {build_name} database.')
    with SQLCursor(path) as cur:
        with open(r'db\init.sql', mode='r') as f:
            script_contents = f.read()
            cur.executescript(script_contents)


if __name__ == '__main__':

    build_name = sys.argv[1]

    start(build_name, True)