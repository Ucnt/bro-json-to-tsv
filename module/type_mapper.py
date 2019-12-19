#!/usr/bin/env python3
'''

Author: Matt Svensson

Purpose: Get the type of file you are given, by its line.

Method: If all of the fields in a line of JSOn are in the fields of a TSV, it is that type of file.

'''
import json

fields_dict = {
    "conn" : ["ts", "uid", "id.orig_h", "id.orig_p", "id.resp_h", "id.resp_p", "proto", "service", "duration", "orig_bytes", "resp_bytes", "conn_state", "local_orig", "local_resp", "missed_bytes", "history", "orig_pkts", "orig_ip_bytes", "resp_pkts", "resp_ip_bytes", "tunnel_parents", "orig_cc", "resp_cc", "sensorname"],
    "dns" : ["ts", "uid", "id.orig_h", "id.orig_p", "id.resp_h", "id.resp_p", "proto", "trans_id", "rtt", "query", "qclass", "qclass_name", "qtype", "qtype_name", "rcode", "rcode_name", "AA", "TC", "RD", "RA", "Z", "answers", "TTLs", "rejected"],
    "http": ["ts", "uid", "id.orig_h", "id.orig_p", "id.resp_h", "id.resp_p", "trans_depth", "method", "host", "uri", "referrer", "version", "user_agent", "origin", "request_body_len", "response_body_len", "status_code", "status_msg", "info_code", "info_msg", "tags", "username", "password", "proxied", "orig_fuids", "orig_filenames", "orig_mime_types", "resp_fuids", "resp_filenames", "resp_mime_types"],
    "ssl" : ["ts", "uid", "id.orig_h", "id.orig_p", "id.resp_h", "id.resp_p", "version", "cipher", "curve", "server_name", "resumed", "last_alert", "next_protocol", "established", "cert_chain_fuids", "client_cert_chain_fuids", "subject", "issuer", "client_subject", "client_issuer", "validation_status", "ja3", "ja3s"],
}

types_dict = {
    "conn" : ["time", "string", "addr", "port", "addr", "port", "enum", "string", "interval", "count", "count", "string", "bool", "bool", "count", "string", "count", "count", "count", "count", "set[string]", "string", "string", "string"],
    "dns" : ["time", "string", "addr", "port", "addr", "port", "enum", "count", "interval", "string", "count", "string", "count", "string", "count", "string", "bool", "bool", "bool", "bool", "count", "vector[string]", "vector[interval]", "bool"],
    "http": ["time", "string", "addr", "port", "addr", "port", "count", "string", "string", "string", "string", "string", "string", "count", "count", "count", "string", "count", "string", "set[enum]", "string", "string", "set[string]", "vector[string]", "vector[string]", "vector[string]", "vector[string]", "vector[string]", "vector[string]"],
    "ssl" : ["time", "string", "addr", "port", "addr", "port", "string", "string", "string", "string", "bool", "string", "string", "bool", "vector[string]", "vector[string]", "string", "string", "string", "string", "string", "string", "string"],
}


def get_type(line):
    try:
        line_json = json.loads(line.strip())
        for file_type in fields_dict.keys():
            if all(key in fields_dict[file_type] for key in line_json.keys()):
                return file_type
        return ""
    except Exception as e:
        print("Error getting type from %s - Error: %s" % (line, str(e)))