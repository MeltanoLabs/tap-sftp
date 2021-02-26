from unittest.mock import patch
from tap_sftp.aws_ssm import AWS_SSM


class MockClient:
    def __init__(self):
        pass
    def get_parameter(self, *args, **kwargs):
        return {'Parameter': {'Value': 'data'}}


@patch('tap_sftp.aws_ssm.boto3.client')
def test_sync_stream_no_tables(patch_client):
    """
        Call the method twice and make sure it shares a client by checking it was only called once
    """
    patch_client.return_value = MockClient()
    ssm_key = AWS_SSM.get_decryption_key('test_key_name')
    assert ssm_key == 'data'
    # call again to make sure it shares the existing connection
    AWS_SSM.get_decryption_key('test_key_name')
    patch_client.assert_called_once()
    