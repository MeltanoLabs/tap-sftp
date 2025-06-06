# Changelog

## 2.2.0

  * Bump dependencies, modernize packaging and drop support for Python 3.8 and below

## 1.0.2
  * If paramiko returns to us a null `st_mtime` for a file then default to utcnow to force the file to sync
