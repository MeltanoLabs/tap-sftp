import io
from datetime import datetime, timezone
from unittest.mock import patch

import pytest
from singer.catalog import Catalog
from tap_sftp.sync import sync_file, sync_stream
from tests.configuration.fixtures import get_sample_file_path, sftp_client


@patch('tap_sftp.client.connection')
def test_sync_stream_no_tables_selected(patch_conn):
    config = {'start_date': '2021-01-01', 'tables': []}
    stream = Catalog.from_dict(
        {
            "streams": [
                    {
                        'tap_stream_id': 'TestStream',
                        'stream': 'TestStream',
                        'schema': {}
                    }
            ]
        }
    ).streams[0]
    result = sync_stream(config, {}, stream)
    assert result == 0


@patch('tap_sftp.sync.sync_file', return_value=1)
@patch('tap_sftp.client.SFTPConnection.get_files_by_prefix')
def test_sync_stream(patch_files, patch_sync_file):
    patch_files.return_value = [
        {'filepath': '/Export/TestStream.txt', 'last_modified': datetime.now(timezone.utc)}
    ]
    config = {
        'start_date': '2021-01-01',
        'host': '',
        'username': '',
        'tables': [
            {
                'table_name': 'TestStream',
                'search_prefix': '/Export',
                'search_pattern': 'TestStream*',
                'key_properties': [],
                'delimiter': ','
            }
        ]
    }
    stream = Catalog.from_dict(
        {
            "streams": [
                    {
                        'tap_stream_id': 'TestStream',
                        'stream': 'TestStream',
                        'schema': {}
                    }
            ]
        }
    ).streams[0]
    result = sync_stream(config, {}, stream)
    assert result == 1
    patch_sync_file.assert_called()


@patch('singer.write_record')
@patch('tap_sftp.client.SFTPConnection.get_file_handle')
def test_sync_file(mock_file_handle, patch_write, sftp_client):
    file_conf = {'filepath': 'fake_file.txt', 'last_modified': ''}
    with open(get_sample_file_path('fake_file.txt'), 'rb') as f:
        mock_file_handle.return_value = f
        stream = Catalog.from_dict(
            {
                "streams": [
                        {
                            'tap_stream_id': 'TestStream',
                            'stream': 'TestStream',
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
                            "metadata": []
                        }
                ]
            }
        ).streams[0]
        table_spec = {
                'table_name': 'TestStream',
                'search_prefix': '/Export',
                'search_pattern': 'TestStream*',
                'key_properties': [],
                'delimiter': ','
        }
        config = {}
        synced_records = sync_file(sftp_client, file_conf, stream, table_spec, config)
        assert synced_records == 1
        patch_write.assert_called_with(
            'TestStream',
            {'Col1': 'data1', 'Col2': 'data2'}
        )

@patch('singer.write_record')
@patch('tap_sftp.client.SFTPConnection.get_file_handle')
def test_sync_file_decrypt(mock_file_handle, patch_write, sftp_client):
    file_conf = {'filepath': 'fake_file.txt', 'last_modified': ''}
    with open(get_sample_file_path('fake_file.txt'), 'rb') as f:
        mock_file_handle.return_value = f
        stream = Catalog.from_dict(
            {
                "streams": [
                        {
                            'tap_stream_id': 'TestStream',
                            'stream': 'TestStream',
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
                            "metadata": []
                        }
                ]
            }
        ).streams[0]
        table_spec = {
                'table_name': 'TestStream',
                'search_prefix': '/Export',
                'search_pattern': 'TestStream*',
                'key_properties': [],
                'delimiter': ','
        }
        config = {}
        synced_records = sync_file(sftp_client, file_conf, stream, table_spec, config)
        assert synced_records == 1
        patch_write.assert_called_with(
            'TestStream',
            {'Col1': 'data1', 'Col2': 'data2'}
        )
