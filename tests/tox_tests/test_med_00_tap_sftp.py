from unittest.mock import patch

from tap_nicesftp.tap import do_discover, do_sync
from tests.configuration.fixtures import get_catalog, get_table_spec

# @patch('tap_sftp.tap.sync_stream')
# def test_sync(patch_sync_stream):
#     catalog = get_catalog()
#     config = {
#         'start_date': '2021-01-01',
#         'host': '',
#         'username': '',
#         'tables': [get_table_spec()]
#     }
#     do_sync(config, catalog, None)
#     patch_sync_stream.assert_called()


@patch('tap_sftp.tap.discover_streams')
def test_discover(patch_discover_stream):
    patch_discover_stream.return_value = {'fake_stream': ''}
    config = {
        'start_date': '2021-01-01',
        'host': '',
        'username': '',
        'tables': [get_table_spec()]
    }
    do_discover(config)
    patch_discover_stream.assert_called()
