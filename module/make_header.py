#!/usr/bin/env python3
'''

Author: Matt Svensson

Purpose: Return the TSV header given a file type.

'''
from module.type_mapper import fields_dict, types_dict


def make_header(file_type):
    fd = fields_dict[file_type]
    if file_type == "http":
        fd.remove('origin')

    header = '''
#separator \\x09
#set_separator	,
#empty_field	(empty)
#unset_field	-
#path	%s
#open	0000-00-00-00-00-00
#fields	%s
#types	%s''' % (file_type, "\t".join(fd), "\t".join(types_dict[file_type]))
    return header.strip()
