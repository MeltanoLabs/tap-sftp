from unittest.mock import patch

from tap_nicesftp.decrypt import gpg_decrypt
from tests.configuration.fixtures import get_sample_file_path


class MockGPG:
    import_cnt = 0
    decrypt_cnt = 0

    def import_keys(self, *args, **kwargs):
        self.import_cnt += 1

    def decrypt_file(self, *args, **kwargs):
        self.decrypt_cnt += 1


@patch('tap_sftp.decrypt.gnupg.GPG')
def test_decrypt(patch_gpg):
    """
        Using the custom mock we assert that keys were imported, file was decrypted, and
        gpg was removed from file name
    """
    gpg = MockGPG()
    patch_gpg.return_value = gpg
    output_path = '/tmp/path'
    key = ''
    gnupghome = ''
    passphrase = ''
    decrypted_path = gpg_decrypt(get_sample_file_path('fake_file.zip.gpg'), output_path, key, gnupghome, passphrase)
    assert decrypted_path == '/tmp/path/fake_file.zip'
    assert gpg.import_cnt == 1
    assert gpg.decrypt_cnt == 1
