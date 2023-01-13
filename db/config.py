import sys
from SQLCursor import SQLCursor


TEST_SQLITE_PATH = 'hqcpq-test.sqlite3'
PRODUCTION_SQLITE_PATH = 'hqcpq.sqlite3'


builds = {
    'test': TEST_SQLITE_PATH,
    'production': PRODUCTION_SQLITE_PATH
}


def start(build_name):

    if build_name not in builds.keys():
        print(f'build name: {build_name} not recognised.')
        return
    
    path = builds[build_name]

    with SQLCursor(path) as cur:
        with open(r'init.sql', mode='r') as f:
            script_contents = f.read()
            cur.executescript(script_contents)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        build_name = sys.argv[1]
    else:
        build_name = 'test'

    print(f'starting with {build_name} database.')
    start(build_name)