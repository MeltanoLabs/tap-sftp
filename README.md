# tap-sftp

[Singer](https://www.singer.io/) tap that extracts data from SFTP files and produces JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md).

## Install:

First, make sure Python 3 is installed on your system or follow these
installation instructions for [Mac](http://docs.python-guide.org/en/latest/starting/install3/osx/) or
[Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-ubuntu-16-04).

It's recommended to use a virtualenv:

```bash
$ python3 -m venv venv
$ pip install tap-sftp
```

or

```bash
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install --upgrade pip
$ pip install .
```

## Configuration:

Create a `config.json` file with connection details to snowflake.

   ```json
   {
        "host": "SFTP_HOST_NAME",
        "port": 22,
        "username": "YOUR_USER",
        "password": "YOUR_PASS",
        "tables": [
            {
                "table_name": "MyExportData",
                "search_prefix": "\/Export\/SubFolder",
                "search_pattern": "MyExportData.*\\.zip.gpg$",
                "key_properties": [],
                "delimiter": ",",
                "encoding": "utf-8",
                "sanitize_header": false
            }
        ],
        "start_date":"2021-01-28",
        "decryption_configs": {
            "SSM_key_name": "SSM_PARAMETER_KEY_NAME",
            "gnupghome": "/your/dir/.gnupg",
            "passphrase": "your_gpg_passphrase"
        },
        "private_key_file": "Optional_Path",
    }
   ```
   If using the decryption feature you must pass the configs shown above, including the AWS SSM parameter name for where the decryption private key is stored. In order to retrieve this parameter the runtime environment must have access to SSM through IAM environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN).

   The following fields are required for the connection configuration:
   - `host`: Hostname or IP of the SFTP server
   - `username`: Username for the SFTP server
   - `port`: Port number for the SFTP server
   - `tables`: An array of tables to load. See table configuration below
   - `start_date`: Earliest file date to synchronize
   - either `password` or `private_key_file`: Authentication to the SFTP Server


   The following table configuration fields are required:
   - `table_name`: The name that should be given to the table (stream)
   - `search_prefix`: Folder where the files are located
   - `search_pattern`: Regex pattern to match the file names
   - `delimiter`: A one-character string delimiter used to separate fields. Default, is `,`.

   The following table configuration fields are optional:
   - `key_properties`: Array containing the unique keys of the table. Defaults to `['_sdc_source_file', '_sdc_source_lineno']`, representing the file name and line number. Specify an emtpy array (`[]`) to load all new files without a replication key
   - `encoding`: File encoding, defaults to `utf-8`
   - `sanitize_header`: Boolean, specifies whether to clean up header names so that they are more likely to be accepted by a target SQL database

## Discovery mode:

The tap can be invoked in discovery mode to find the available tables and
columns in the database:

```bash
$ tap-sftp --config config.json --discover > catalog.json
```

A discovered catalog is output, with a JSON-schema description of each table. A
source table directly corresponds to a Singer stream.

Edit the `catalog.json` and select the streams to replicate. Or use this helpful [discovery utility](https://github.com/chrisgoddard/singer-discover).

## Run Tap:

Run the tap like any other singer compatible tap:

```
$ tap-sftp --config config.json --catalog catalog.json --state state.json
```

## To run tests:

1. Install python dependencies in a virtual env and run unit and integration tests
```
  python3 -m venv venv
  . venv/bin/activate
  pip install --upgrade pip
  pip install .
  pip install tox
```

2. To run unit tests:
```
  tox
```

## License

Apache License Version 2.0

See [LICENSE](LICENSE) to see the full text.
