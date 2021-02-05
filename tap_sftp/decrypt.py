import io
import os

import gnupg


def gpg_decrypt_to_file(gpg, file_obj, file_path):
    decrypted_path = os.path.splitext(file_path)[0]
    gpg.decrypt_file(file_obj, output=decrypted_path)
    return decrypted_path

def initialize_gpg(key_paths):
    gpg = gnupg.GPG(gnupghome="/.gnupg")
    for path in key_paths:
        key_data = open(path).read()
        gpg.import_keys(key_data)
    return gpg

def gpg_decrypt(file_obj, file_name):
    gpg = initialize_gpg(['.ssh/sfmc.gpg'])
    file_name = ''
    decrypted_path = gpg_decrypt_to_file(gpg, file_obj, file_name)
    return open(decrypted_path, 'rb')
