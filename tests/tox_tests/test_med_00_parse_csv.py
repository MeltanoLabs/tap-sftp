from tap_sftp.singer_encodings import csv_handler
from tests.configuration.fixtures import get_sample_file_path

def test_sanitize_headers():
    """Test the parser."""
    options = {
        'delimiter': ',',
        'key_properties': ['id'],
        'sanitize_headers': True,
    }

    with open(get_sample_file_path('unsanitized_file.csv'), 'rb') as file:
        parser = csv_handler.get_row_iterator(file, options=options)



    assert parser.fieldnames == ['id', 'col_2_']


def test_no_sanitized_headers():
    """Test the parser."""
    options = {
        'delimiter': ',',
        'key_properties': ['id'],
        'sanitize_headers': False,
    }

    with open(get_sample_file_path('unsanitized_file.csv'), 'rb') as file:

        parser = csv_handler.get_row_iterator(file, options=options)
        
    assert parser.fieldnames == ['id', 'Col($2)']