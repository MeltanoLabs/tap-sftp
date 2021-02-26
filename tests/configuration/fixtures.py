from pathlib import Path
from unittest.mock import Mock, patch, PropertyMock

from pytest import fixture
from singer.catalog import Catalog
from tap_sftp.client import connection


class MockSFTPClient:

    def __init__(self, *args, **kwargs):
        pass
    def get(self, *args, **kwargs):
        pass
    def close(self, *args, **kwargs):
        pass

@fixture
def sftp_client(monkeypatch):
    # overwrite the client so we never actually try to connect to an sftp
    monkeypatch.setattr('paramiko.SFTPClient.from_transport', MockSFTPClient)
    config = {
        'host': '',
        'username': ''
    }
    return connection(config)

def get_sample_file_path(file_name):
    path = Path(__file__).parent.absolute()
    return f'{path}/{file_name}'

def get_catalog():
    return Catalog.from_dict(
        {
            "streams": [
                    {
                        'tap_stream_id': 'fake_file',
                        'stream': 'fake_file',
                        'schema': {
                            "type": "object",
                            "properties": {
                                "Col1": {
                                    "type": [
                                        "null",
                                        "string"
                                    ]
                                },
                                "Col2": {
                                    "type": [
                                        "null",
                                        "string"
                                    ]
                                }
                            }
                        },
                        "metadata": [
                            {
                                "breadcrumb": [],
                                "metadata": {
                                    "table-key-properties": [],
                                    "forced-replication-method": "INCREMENTAL",
                                    "selected": True,
                                    "inclusion": "available"
                                }
                            }
                        ]
                    }
            ]
        }
    )


def get_table_spec():
    return {
        'table_name': 'fake_file',
        'search_prefix': '/Export',
        'search_pattern': 'fake_file*',
        'key_properties': [],
        'delimiter': ','
    }