import json
import sys

import singer
from singer import metadata, utils
from terminaltables import AsciiTable
from tap_sftp import client, stats

from tap_sftp.discover import discover_streams
from tap_sftp.stats import STATS
from tap_sftp.sync import sync_stream

REQUIRED_CONFIG_KEYS = ["username", "port", "host", "tables", "start_date"]
REQUIRED_DECRYPT_CONFIG_KEYS = ['SSM_key_name', 'gnupghome', 'passphrase']
REQUIRED_TABLE_SPEC_CONFIG_KEYS = ["key_properties", "delimiter", "table_name", "search_prefix", "search_pattern"]

LOGGER = singer.get_logger()


def do_discover(config):
    LOGGER.info("Starting discover")
    streams = discover_streams(config)
    if not streams:
        raise Exception("No streams found")
    catalog = {"streams": streams}
    json.dump(catalog, sys.stdout, indent=2)
    LOGGER.info("Finished discover")


def stream_is_selected(mdata):
    return mdata.get((), {}).get('selected', False)


def do_sync(config, catalog, state):
    LOGGER.info('Starting sync.')
    sftp_client = client.connection(config)

    for stream in catalog.streams:
        stream_name = stream.tap_stream_id
        mdata = metadata.to_map(stream.metadata)

        if not stream_is_selected(mdata):
            LOGGER.info("%s: Skipping - not selected", stream_name)
            continue

        singer.write_state(state)
        key_properties = metadata.get(metadata.to_map(stream.metadata), (), "table-key-properties")
        singer.write_schema(stream_name, stream.schema.to_dict(), key_properties)

        LOGGER.info("%s: Starting sync", stream_name)
        counter_value = sync_stream(config, state, stream, sftp_client)
        LOGGER.info("%s: Completed sync (%s rows)", stream_name, counter_value)

    headers = [['table_name',
                'search prefix',
                'search pattern',
                'file path',
                'row count',
                'last_modified']]

    rows = []

    for table_name, table_data in STATS.items():
        for filepath, file_data in table_data['files'].items():
            rows.append([table_name,
                         table_data['search_prefix'],
                         table_data['search_pattern'],
                         filepath,
                         file_data['row_count'],
                         file_data['last_modified']])

    data = headers + rows
    table = AsciiTable(data, title='Extraction Summary')

    sftp_client.close()
    LOGGER.info("\n\n%s", table.table)
    LOGGER.info('Done syncing.')


@singer.utils.handle_top_exception(LOGGER)
def main():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    # validate tables config
    for table in args.config.get('tables'):
        utils.check_config(table, REQUIRED_TABLE_SPEC_CONFIG_KEYS)

    decrypt_configs = args.config.get('decryption_configs')
    if decrypt_configs:
        # validate decryption configs
        utils.check_config(decrypt_configs, REQUIRED_DECRYPT_CONFIG_KEYS)

    if args.discover:
        do_discover(args.config)
    elif args.catalog or args.properties:
        do_sync(args.config, args.catalog, args.state)
