import json

import singer
from singer import Transformer, metadata, utils

from tap_sftp import client, stats
from tap_sftp.aws_ssm import AWS_SSM
from tap_sftp.singer_encodings import compression, csv_handler

LOGGER = singer.get_logger()


def sync_stream(config, state, stream):
    table_name = stream.tap_stream_id
    modified_since = utils.strptime_to_utc(singer.get_bookmark(state, table_name, 'modified_since') or
                                           config['start_date'])

    LOGGER.info('Syncing table "%s".', table_name)
    LOGGER.info('Getting files modified since %s.', modified_since)

    conn = client.connection(config)
    table_spec = [table_config for table_config in config["tables"] if table_config["table_name"] == table_name]
    if len(table_spec) == 0:
        LOGGER.info("No table configuration found for '%s', skipping stream", table_name)
        return 0
    if len(table_spec) > 1:
        LOGGER.info("Multiple table configurations found for '%s', skipping stream", table_name)
        return 0
    table_spec = table_spec[0]

    files = conn.get_files(table_spec["search_prefix"],
                           table_spec["search_pattern"],
                           modified_since)

    LOGGER.info('Found %s files to be synced.', len(files))

    records_streamed = 0
    if not files:
        return records_streamed

    for f in files:
        records_streamed += sync_file(conn, f, stream, table_spec, config)
        state = singer.write_bookmark(state, table_name, 'modified_since', f['last_modified'].isoformat())
        singer.write_state(state)

    LOGGER.info('Wrote %s records for table "%s".', records_streamed, table_name)

    return records_streamed


def sync_file(conn, f, stream, table_spec, config):
    LOGGER.info('Syncing file "%s".', f["filepath"])
    decryption_configs = config.get('decryption_configs')
    if decryption_configs:
        decryption_configs['key'] = AWS_SSM.get_decryption_key(decryption_configs.get('SSM_key_name'))
        file_handle, decrypted_name = conn.get_file_handle(f, decryption_configs)
        f['filepath'] = decrypted_name
    else:
        file_handle = conn.get_file_handle(f)

    # Add file_name to opts and flag infer_compression to support gzipped files
    opts = {'key_properties': table_spec['key_properties'],
            'delimiter': table_spec['delimiter'],
            'file_name': f['filepath']}

    readers = csv_handler.get_row_iterators(file_handle, options=opts, infer_compression=True)

    records_synced = 0

    for reader in readers:
        with Transformer() as transformer:
            for row in reader:
                custom_columns = {
                    '_sdc_source_file': f["filepath"],

                    # index zero, +1 for header row
                    '_sdc_source_lineno': records_synced + 2
                }
                rec = {**row, **custom_columns}

                to_write = transformer.transform(rec, stream.schema.to_dict(), metadata.to_map(stream.metadata))

                singer.write_record(stream.tap_stream_id, to_write)
                records_synced += 1
                if records_synced % 10000 == 0:
                    LOGGER.info(f'Synced Record Count: {records_synced}')

    stats.add_file_data(table_spec, f['filepath'], f['last_modified'], records_synced)

    return records_synced
