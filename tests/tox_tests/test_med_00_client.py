from unittest.mock import patch

import pytest
from tests.configuration.fixtures import get_sample_file_path, sftp_client
from datetime import datetime


@patch('tap_sftp.client.SFTPConnection.sftp')
@patch('tempfile.TemporaryDirectory.__enter__', return_value=get_sample_file_path(''))
def test_get_file_handle(patch_temp, patch_sftp, sftp_client):
    """
        Patch the temp file location and the sftp conn. Confirms no errors reading the file after sftp get 
    """
    sftp_client.get_file_handle({'filepath': '/fake_file.txt'})


@patch('tap_sftp.decrypt.gpg_decrypt', return_value=get_sample_file_path('fake_file.txt'))
@patch('tap_sftp.client.SFTPConnection.sftp')
def test_get_file_handle_decrypt(patch_sftp, patch_decrypt, sftp_client):
    """
        File handle of gpg file calls the decrypt method
    """
    sftp_client.get_file_handle({'filepath': '/path'}, {'key': 'key', 'gnupghome': 'gnupghome', 'passphrase': 'passphrase'})
    patch_decrypt.assert_called()

@patch('tap_sftp.decrypt.gpg_decrypt')
@patch('tap_sftp.client.SFTPConnection.sftp')
def test_get_file_handle_decrypt_failed(patch_sftp, patch_decrypt, sftp_client):
    """
        Exception is raised if decryption fails
    """
    patch_decrypt.return_value = get_sample_file_path('doesnt_exist.txt')
    with pytest.raises(Exception):
        sftp_client.get_file_handle({'filepath': '/path'}, {'key': 'key', 'gnupghome': 'gnupghome', 'passphrase': 'passphrase'})
