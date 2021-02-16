from pathlib import Path

from pytest import fixture
from tap_sftp.client import connection


@fixture
def sftp_client():
    config = {
        'host': '',
        'username': ''
    }
    return connection(config)


def get_sample_file_path(file_name):
    path = Path(__file__).parent.absolute()
    return f'{path}/{file_name}'
