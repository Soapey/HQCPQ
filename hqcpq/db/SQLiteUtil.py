import os
from sqlite3 import connect
from hqcpq.helpers.io import read_config, join_to_project_folder


def default_path():
    config = read_config()

    project_path_fallback = join_to_project_folder(os.path.join("hqcpq", "db", "hqcpq.db"))

    database_path_value = config.get("DB", "database_path", fallback=str())
    if not os.path.exists(database_path_value):
        database_path_value = None

    return database_path_value or project_path_fallback


def initialise_db(clear: bool = False):
    database_path = default_path()
    if clear and os.path.exists(database_path):
        os.remove(database_path)

    with SQLiteConnection() as cur:
        init_script_path = join_to_project_folder(os.path.join("hqcpq", "db", "init.sql"))
        with open(init_script_path, "r") as init_file:
            init_script = init_file.read()
            cur.executescript(init_script)


class SQLiteConnection:
    def __init__(self):
        self.database_path = default_path()
        self.connection = None

    def __enter__(self):
        self.connection = connect(self.database_path)
        self.connection.execute("PRAGMA foreign_keys = ON")
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()
