# mdb_conv
---

Converts MDB (.mdb) file to Excel file (.xls).

Dependencies (for non Windows 7 32 bit):
pyodbc drivers are available at https://code.google.com/p/pyodbc/downloads/list

Instructions:
1. Place excel file relative to this script.
2. Run this command.
`python mdb_conv.py somedb.mdb`

Bugs:
1. bytearray type not compatible for tablib, for export to excel file.