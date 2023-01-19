import sys
import os
from app.db.SQLCursor import SQLCursor, builds


def start(build_name: str, clean_start: bool = False):

    if build_name not in builds.keys():
        return
    
    path = builds[build_name]

    if clean_start and os.path.exists(path):
        os.remove(path)
        
    with SQLCursor() as cur:
        with open(r'app\db\init.sql', mode='r') as f:
            script_contents = f.read()
            cur.executescript(script_contents)


if __name__ == '__main__':

    build_name = sys.argv[1]

    start(build_name, True)