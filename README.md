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

1. Create a `config.json` file with connection details to snowflake.

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
                "encoding": "utf-8"
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

   The private_key_file is optional.

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
