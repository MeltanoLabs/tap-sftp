from tap_sftp.singer_encodings.compression import infer
from tests.configuration.fixtures import get_sample_file_path


def test_infer_compression():
    """
        Reading the test zip file it infers file type and unzips properly
    """
    with open(get_sample_file_path('fake_file.txt.zip'), 'rb') as f:
        out = infer(f, 'fake_file.txt.zip')
        assert next(out).read() == b'Col1,Col2\ndata1,data2\n'
