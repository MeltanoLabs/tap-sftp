.DEFAULT_GOAL := test

test:
	pylint tap_nicesftp -d missing-docstring,fixme,duplicate-code,line-too-long
