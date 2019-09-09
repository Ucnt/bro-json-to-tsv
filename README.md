# Bro JSON to TSV

## Purpose
Covert Bro JSON files (specifically, conn, dns, http and ssl) in the input_folder to TSV in the output_folder 

## Background
Active Countermeasures (https://www.activecountermeasures.com/) has an awesome project called RITA (https://github.com/activecm/rita) that analyzes bro, TSV, telemetry to look for beaconing, DNS tunneling, and blacklist hits.

Security Onion, by default, creates the bro telemetry as JSON.  Several vendors I used needed JSON so the easiest thing was to create a converter.

## Architecture

The optimal way to use this script is to:

1. Get your logs onto the same box that RITA is installed on
2. Convert those logs with these scripts
3. Use a rolling import of the converted logs into RITA

As an example, below is the methodology I use:

1. On each Security Onion worker, use google-fluentd to send conn, dns, http, and ssl logs to Stackdriver.  (Alternately, you could add a new syslog destination for those logs via /etc/syslog-ng/syslog.conf)
2. Export those logs from Stackdriver to GCS (occurs hourly)
3. An hourly cronjob, on the RITA box, downloads the new logs from GCS, converts them using these scripts, and imports the logs into RITA.

## Requirements

* python3, python3-pip
* Libraries: tqdm  (can be installed with pip3 install -r requirements.txt)

## Execution

python3 run_parser.py --input_folder /json/folder/path --output_folder /output/folder/path

## Methodology

* gunzip the files in the input folder if they are compressed
* For every file in the input folder path:
  * Check the first line of the file to see what file type it is (e.g. conn, by checking the keys in the dict)
  * Add the TSV header to the output file
  * Add each JSON line as a TSV to the output file

## Notes

* Be careful with module/make_header.py.  The header format is finicky, e.g. most items are separated by tabs, not spaces.  Modifying it (e.g. converting the tabs to 4 spaces) will break TSV readers/parsers.
