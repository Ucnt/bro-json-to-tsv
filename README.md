# Bro JSON to TSV

## Purpose

Covert Bro JSON files (specifically, conn, dns, http and ssl) in the input_folder to TSV in the output_folder 

## Background

Black Hills Information Security has an awesome project called RITA (https://www.blackhillsinfosec.com/projects/rita/) that analyzes bro, TSV, telemetry.

Security Onion, by default, creates the bro telemetry as JSON and, for me as an example, several other vendors only take JSON.  So, I needed a way to have both types.


## Requirements

The below can be installed by running the setup.sh script.

* python3, python3-pip
* Libraries: tqdm

## Execution

python3 run_parser.py --input_folder json/folder/path --output_folder output/folder/path

## Methodology

* gunzip the files in the input folder if they are compressed
* For every file in the input folder path:
  * Check the first line of the file to see what file type it is (e.g. conn, by checking the keys in the dict)
  * Add the header for the TSV for the output folder
  * Add each JSON line as a TSV to the output folder

## Notes

* Be careful with module/make_header.py.  The header format is finicky, e.g. most items are separated by tabs, not spaces.  Modifying it (e.g. converting the tabs to 4 spaces) might break TSV readers/parsers.
