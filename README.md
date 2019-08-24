# Bro JSON to TSV

## Purpose

Covert Bro JSON files in the input_folder to TSV in the output_folder (specifically, conn, dns, http and ssl)

## Requirements

    - python3

## Execution

python3 run_parser.py --input_folder json/folder/path --output_folder output/folder/path

## Methodology

    - For every file in the input folder path:

        - Check the first line of the file to see what file type it is (e.g. conn, by checking the keys in the dict)

        - Add the header for the TSV for the output folder

        - Add each JSON line as a TSV to the output folder
