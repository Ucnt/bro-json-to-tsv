#!/usr/bin/env python3
'''

Author: Matt Svensson

Purpose: Convert bro JSON files to JSON TSV files

'''
import subprocess
import os,os.path
from glob import glob
from json_to_tsv import json_to_tsv
from make_header import make_header
from type_mapper import get_type
import multiprocessing
from tqdm import tqdm
import argparse
parser = argparse.ArgumentParser(description='Get input and output folder locations')
parser.add_argument('-i', '--input_folder', required=True,  help='input log folder')
parser.add_argument('-o', '--output_folder',  required=True, help='output log folder')
args = parser.parse_args()
input_folder = args.input_folder
output_folder = args.output_folder


def gunzip_files(input_folder):
    print("Being sure all files in %s are gunzipped" % (input_folder))
    p = subprocess.Popen("gunzip %s/*.gz" % (input_folder), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,)
    output, error = p.communicate()
    p_status = p.wait()
    print("Done gunzipping files in %s" % (input_folder))


def run_file(path, file_name):
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


if __name__ == "__main__":
    # gunzip all the things...
    gunzip_files(input_folder)

    # Setup pool for processing the files
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    # Be sure new folder is created
    try:
        os.mkdir(output_folder)
    except FileExistsError:
        pass

    files = []
    for abs_file_path in [y for x in os.walk(input_folder) for y in glob(os.path.join(x[0], '*'))]:
        path = "%s/" % ("/".join(map(str,(abs_file_path.split("/")[0:len(abs_file_path.split("/"))-1]))))
        file_name = abs_file_path.split("/")[len(abs_file_path.split("/")) - 1]
        files.append([path, file_name])        

    # Run the files
    pbar = tqdm(total=len(files))
    def update(*a):
        pbar.update()
    for path, file_name in files:
        pool.apply_async(run_file, args=(path, file_name, ), callback=update)

    # Keep 'em going!
    pool.close()
    pool.join()
