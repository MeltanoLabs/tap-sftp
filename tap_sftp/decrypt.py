import io
import os

import gnupg


def gpg_decrypt_to_file(gpg, file_obj, sftp_file_path, output_dir, passphrase):
    gpg_filename = os.path.basename(sftp_file_path)
    decrypted_filename = os.path.splitext(gpg_filename)[0]
    decrypted_path = f'{output_dir}/{decrypted_filename}'
    gpg.decrypt_file(file_obj, output=decrypted_path, passphrase=passphrase)
    return decrypted_path


def initialize_gpg(key, gnupghome):
    gpg = gnupg.GPG(gnupghome=gnupghome)
    gpg.import_keys(key)
    return gpg


def gpg_decrypt(file_obj, output_path, sftp_file_path, key, gnupghome, passphrase):
    gpg = initialize_gpg(key, gnupghome)
    return gpg_decrypt_to_file(gpg, file_obj, sftp_file_path, output_path, passphrase)
