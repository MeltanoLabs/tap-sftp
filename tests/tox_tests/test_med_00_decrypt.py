from tap_sftp.decrypt import gpg_decrypt
from unittest.mock import patch


class MockGPG:
    import_cnt = 0
    decrypt_cnt = 0

    def import_keys(self, *args, **kwargs):
        self.import_cnt += 1

    def decrypt_file(self, *args, **kwargs):
        self.decrypt_cnt += 1


@patch('tap_sftp.decrypt.gnupg.GPG')
def test_decrypt(patch_gpg):
    gpg = MockGPG()
    patch_gpg.return_value = gpg
    file_obj = ''
    output_path = '/tmp/path'
    sftp_file_path = '/Export/sftp_dir/file_name.txt.gpg'
    key = ''
    gnupghome = ''
    passphrase = ''
    decrypted_path = gpg_decrypt(file_obj, output_path, sftp_file_path, key, gnupghome, passphrase)
    assert decrypted_path == '/tmp/path/file_name.txt'
    assert gpg.import_cnt == 1
    assert gpg.decrypt_cnt == 1