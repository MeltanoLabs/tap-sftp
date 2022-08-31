from datetime import datetime, timezone
from unittest.mock import patch

from tap_sftp.sync import sync_file, sync_stream
from tests.configuration.fixtures import (get_catalog, get_sample_file_path,
                                          get_table_spec, sftp_client)


@patch('tap_sftp.client.connection')
def test_sync_stream_no_tables_selected(patch_conn, sftp_client):
    """
        Only sync files that are selected in the config
    """
    config = {'start_date': '2021-01-01', 'tables': []}
    stream = get_catalog().streams[0]
    result = sync_stream(config, {}, stream, sftp_client)
    assert result == 0


@patch('tap_sftp.sync.sync_file', return_value=1)
@patch('tap_sftp.client.SFTPConnection.get_files_by_prefix')
def test_sync_stream(patch_files, patch_sync_file, sftp_client):
    """
        Mock out the files returned so that the sync_stream reads our local test files. Assert we processed 1 record
    """
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
    result = sync_stream(config, {}, stream, sftp_client)
    assert result == 1
    patch_sync_file.assert_called()


@patch('singer.write_record')
@patch('tap_sftp.client.SFTPConnection.get_file_handle')
def test_sync_file(mock_file_handle, patch_write, sftp_client):
    """
        Mock the file handle so it reads our test file. Then assert the write_record data is correct.
    """
    file_conf = {'filepath': 'fake_file.txt', 'last_modified': ''}
    with open(get_sample_file_path('fake_file.txt'), 'rb') as f:
        mock_file_handle.return_value = f
        stream = get_catalog().streams[0]
        config = {'host': '', 'username': ''}
        synced_records = sync_file(file_conf, stream, get_table_spec(), config, sftp_client)
        assert synced_records == 1
        patch_write.assert_called_with(
            'fake_file',
            {'Col1': 'data1', 'Col2': 'data2'}
        )


@patch('singer.write_record')
@patch('tap_sftp.aws_ssm.AWS_SSM.get_decryption_key')
@patch('tap_sftp.client.SFTPConnection.get_file_handle')
def test_sync_file_decrypt(mock_file_handle, patch_aws, patch_write, sftp_client):
    """
        Call with decrypt option, mock the file handle so it reads our test file. Then assert the
        write_record data is correct and the decrypted name is the new filepath.
    """
    file_conf = {'filepath': 'fake_file.txt', 'last_modified': ''}
    with open(get_sample_file_path('fake_file.txt'), 'rb') as f:
        mock_file_handle.return_value = f, 'new_file_name.txt'
        stream = get_catalog().streams[0]
        config = {'host': '', 'username': '', 'decryption_configs': {'': ''}}
        synced_records = sync_file(file_conf, stream, get_table_spec(), config, sftp_client)
        assert synced_records == 1
        patch_aws.assert_called()
        patch_write.assert_called_with(
            'fake_file',
            {'Col1': 'data1', 'Col2': 'data2'}
        )
        assert file_conf['filepath'] == 'new_file_name.txt'
