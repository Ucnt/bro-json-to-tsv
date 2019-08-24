#!/usr/bin/env python3
'''

Author: Matt Svensson

Purpose: Convert the line of JSON to a TSV, given its file type (e.g. conn, dhcp, ssl, etc)

'''
from module.json_to_tsv import json_to_tsv
from module.make_header import make_header
from module.type_mapper import get_type

def run_file(path, file_name, output_folder):
    try:
        # Create an output file for the new TSV
        output_file = open("%s/%s" % (output_folder, file_name), "w+")

        # Read in all fo the new file and write new lines to the output file
        first = True
        file_type = ""
        with open ("%s/%s" % (path, file_name), "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if first:
                    file_type = get_type(line=line)
                    if not file_type:
                        print("Can't identify file type of %s%s" % (path, file_name))
                    header = make_header(file_type=file_type)
                    output_file.write("%s\n" % (header))
                    first = False
                line_tsv = json_to_tsv(line=line, file_type=file_type)
                if line_tsv:
                    output_file.write("%s\n" % (line_tsv))

        # Close the new tsv file
        output_file.close()
    except Exception as e:
        print("Error parsing %s%s - %s" % (path, file_name, str(e)))
