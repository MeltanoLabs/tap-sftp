import io
import os

import gnupg


def gpg_decrypt_to_file(gpg, file_obj, sftp_file_path, output_dir):
    gpg_filename = os.path.basename(sftp_file_path)
    decrypted_filename = os.path.splitext(gpg_filename)[0]
    decrypted_path = f'{output_dir}/{decrypted_filename}'
    gpg.decrypt_file(file_obj, output=decrypted_path)
    return decrypted_path

def initialize_gpg(key_paths, gnupghome):
    gpg = gnupg.GPG(gnupghome=gnupghome)
    for path in key_paths:
        key_data = open(path).read()
        gpg.import_keys(key_data)
    return gpg

def gpg_decrypt(file_obj, output_path, sftp_file_path, key_path, gnupghome):
    gpg = initialize_gpg([key_path], gnupghome)
    return gpg_decrypt_to_file(gpg, file_obj, sftp_file_path, output_path)
