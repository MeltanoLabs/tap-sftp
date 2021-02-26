from datetime import datetime, timezone
from unittest.mock import patch

from tap_sftp.discover import discover_streams
from tests.configuration.fixtures import get_sample_file_path, get_table_spec

expected_schema = {
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
                },
                "_sdc_source_file": {
                    "type": "string"
                },
                "_sdc_source_lineno": {
                    "type": "integer"
                },
                "_sdc_extra": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        }

@patch('tap_sftp.client.SFTPConnection.get_files_by_prefix')
@patch('tap_sftp.client.SFTPConnection.get_file_handle')
def test_discover_streams(patch_file_handle, patch_files):
    # mock out the files returned from the sftp list
    patch_files.return_value = [
        {'filepath': '/Export/fake_file.txt', 'last_modified': datetime.now(timezone.utc)}
    ]
    config = {
        'host': '',
        'username': '',
        'tables': [get_table_spec()]
    }
    # mock the file handle using the local fake_file.txt
    with open(get_sample_file_path('fake_file.txt'), 'rb') as f:
        patch_file_handle.return_value = f
        streams = discover_streams(config)
    assert streams[0].get('schema') == expected_schema


@patch('tap_sftp.client.SFTPConnection.get_files_by_prefix')
@patch('tap_sftp.client.SFTPConnection.get_file_handle')
def test_discover_streams_decrypt(patch_file_handle, patch_files):
    # mock out the files returned from the sftp list
    patch_files.return_value = [
        {'filepath': '/Export/fake_file.txt', 'last_modified': datetime.now(timezone.utc)}
    ]
    config = {
        'host': '',
        'username': '',
        'tables': [get_table_spec()],
        'decryption_configs': {
            'SSM_key_name': '',
            'gnupghome': '',
            'passphrase': ''
        }
    }
    # mock the file handle using the local fake_file.txt
    with open(get_sample_file_path('fake_file.txt'), 'rb') as f:
        patch_file_handle.return_value = f, '/temp/path/fake_file.txt'
        streams = discover_streams(config)
    assert streams[0].get('schema') == expected_schema
