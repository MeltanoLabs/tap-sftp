from unittest.mock import patch

import pytest
from tests.configuration.fixtures import get_sample_file_path, sftp_client


class MockSFTP:
    def __init__(self):
        pass
    def open(self, *args, **kwargs):
        return None


@patch('tap_sftp.client.SFTPConnection.sftp')
def test_get_file_handle(patch_sftp, sftp_client):
    patch_sftp.return_value = MockSFTP()
    sftp_client.get_file_handle({'filepath': ''})


@patch('tap_sftp.decrypt.gpg_decrypt')
@patch('tap_sftp.client.SFTPConnection.sftp')
def test_get_file_handle_decrypt(patch_sftp, patch_decrypt, sftp_client):
    patch_sftp.return_value = MockSFTP()
    patch_decrypt.return_value = get_sample_file_path('fake_file.txt')
    sftp_client.get_file_handle({'filepath': '/path'}, {'key': 'key', 'gnupghome': 'gnupghome', 'passphrase': 'passphrase'})
    patch_decrypt.assert_called()

@patch('tap_sftp.decrypt.gpg_decrypt')
@patch('tap_sftp.client.SFTPConnection.sftp')
def test_get_file_handle_decrypt_failed(patch_sftp, patch_decrypt, sftp_client):
    patch_sftp.return_value = MockSFTP()
    patch_decrypt.return_value = get_sample_file_path('doesnt_exist.txt')
    with pytest.raises(Exception):
        sftp_client.get_file_handle({'filepath': '/path'}, {'key': 'key', 'gnupghome': 'gnupghome', 'passphrase': 'passphrase'})
