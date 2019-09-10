#!/usr/bin/env python3
'''

Author: Matt Svensson

Purpose: Convert the line of JSON to a TSV, given its file type (e.g. conn, dhcp, ssl, etc)

'''
from module.json_to_tsv import json_to_tsv
from module.make_header import make_header
from module.type_mapper import get_type

def run_file(full_path_old, full_path_new):
    try:
        output_file = open(full_path_new, "w+")

        # Read in all fo the new file and write new lines to the output file
        first = True
        file_type = ""
        with open (full_path_old, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if first:
                    file_type = get_type(line=line)
                    if not file_type:
                        print("Can't identify file type of %s" % (full_path_old))
                    header = make_header(file_type=file_type)
                    output_file.write("%s\n" % (header))
                    first = False
                elif file_type != "":
                    line_tsv = json_to_tsv(line=line, file_type=file_type)
                    if line_tsv:
                        output_file.write("%s\n" % (line_tsv))

        # Close the new tsv file
        output_file.close()
    except Exception as e:
        print("Error parsing %s - %s" % (full_path_old, str(e)))
