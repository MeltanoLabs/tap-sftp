import io
from datetime import datetime, timezone
from unittest.mock import patch

import pytest
from tap_sftp.sync import sync_file, sync_stream
from tests.configuration.fixtures import (get_catalog, get_sample_file_path,
                                          get_table_spec, sftp_client)


@patch('tap_sftp.client.connection')
def test_sync_stream_no_tables_selected(patch_conn):
    config = {'start_date': '2021-01-01', 'tables': []}
    stream = get_catalog().streams[0]
    result = sync_stream(config, {}, stream)
    assert result == 0


@patch('tap_sftp.sync.sync_file', return_value=1)
@patch('tap_sftp.client.SFTPConnection.get_files_by_prefix')
def test_sync_stream(patch_files, patch_sync_file):
    patch_files.return_value = [
        {'filepath': '/Export/fake_file.txt', 'last_modified': datetime.now(timezone.utc)}
    ]
    config = {
        'start_date': '2021-01-01',
        'host': '',
        'username': '',
        'tables': [get_table_spec()]
    }
    stream = get_catalog().streams[0]
    result = sync_stream(config, {}, stream)
    assert result == 1
    patch_sync_file.assert_called()


@patch('singer.write_record')
@patch('tap_sftp.client.SFTPConnection.get_file_handle')
def test_sync_file(mock_file_handle, patch_write, sftp_client):
    file_conf = {'filepath': 'fake_file.txt', 'last_modified': ''}
    with open(get_sample_file_path('fake_file.txt'), 'rb') as f:
        mock_file_handle.return_value = f
        stream = get_catalog().streams[0]
        config = {}
        synced_records = sync_file(sftp_client, file_conf, stream, get_table_spec(), config)
        assert synced_records == 1
        patch_write.assert_called_with(
            'fake_file',
            {'Col1': 'data1', 'Col2': 'data2'}
        )


@patch('singer.write_record')
@patch('tap_sftp.client.SFTPConnection.get_file_handle')
def test_sync_file_decrypt(mock_file_handle, patch_write, sftp_client):
    file_conf = {'filepath': 'fake_file.txt', 'last_modified': ''}
    with open(get_sample_file_path('fake_file.txt'), 'rb') as f:
        mock_file_handle.return_value = f
        stream = get_catalog().streams[0]
        config = {}
        synced_records = sync_file(sftp_client, file_conf, stream, get_table_spec(), config)
        assert synced_records == 1
        patch_write.assert_called_with(
            'fake_file',
            {'Col1': 'data1', 'Col2': 'data2'}
        )
