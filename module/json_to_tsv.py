#!/usr/bin/env python3
'''

Author: Matt Svensson

Purpose: Convert the line of JSON to a TSV, given its file type (e.g. conn, dhcp, ssl, etc)

'''
import json
import time
import datetime
from module.type_mapper import fields_dict


def json_to_tsv(line, file_type):
    try:
        # Parse the line into json
        line_json = json.loads(line.strip())

        fields = []
        for field in fields_dict[file_type]:
            try:
                if field == "ts":
                    d = datetime.datetime.strptime(line_json[field], '%Y-%m-%dT%H:%M:%S.%fZ')
                    fields.append("%s.%s" % (d.strftime("%s"), d.microsecond))
                else:
                    fields.append(line_json[field])
            except Exception as e:
                fields.append("-")

        line_tsv = "\t".join((map(str,fields)))
        return line_tsv
    except Exception as e:
        print("Error parsing line %s - Error: %s" (line, str(e)))