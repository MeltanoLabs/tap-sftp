.DEFAULT_GOAL := test

test:
	uvx pylint tap_sftp -d missing-docstring,fixme,duplicate-code,line-too-long
