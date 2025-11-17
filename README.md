# PondCDRTools

![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A collection of Python scripts for working with CDR (Call Detail Records) files.

## Scripts

### cdr_copy.py
Use case: Organizes CDR files from a source directory by copying files from a specific month/year and distributing them into client-specific subfolders in a target directory. Helpful for monthly processing and archiving of call records.

### cdr_find.py
Use case: Searches through CDR files in a directory to find all files containing a specific CDR_ID. Useful for locating specific call records across multiple files in a folder.

## Usage

No installation required - uses only standard Python libraries.

Run any script with:
```bash
python script_name.py
