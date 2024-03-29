import configparser
import os


def join_to_project_folder(relative_path):

    base_path = os.path.abspath(".")

    full_path = os.path.join(base_path, relative_path)

    return full_path


def default_config_path():
    return join_to_project_folder(os.path.join("hqcpq", "config.ini"))

def read_config(config_file_path: str = None):

    if not config_file_path:
        config_file_path = default_config_path()

    config_parser = configparser.ConfigParser()
    config_parser.read(config_file_path)

    return config_parser


def update_config(config_parser: configparser.ConfigParser, config_file_path: str = None):

    if not config_file_path:
        config_file_path = default_config_path()

    with open(config_file_path, "w+") as config_file:
        config_parser.write(config_file)

def email_body_path():
    return join_to_project_folder(os.path.join("hqcpq", "quote_email_body.txt"))


def get_email_body():
    email_body = str()
    with open(email_body_path(), 'r') as file:
        email_body = file.read()
    return email_body


def get_documents_directory():
    home_directory = os.path.expanduser('~')
    return os.path.join(home_directory, 'Documents')