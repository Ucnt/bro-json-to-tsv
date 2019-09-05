#!/usr/bin/env python3
'''

Author: Matt Svensson

Purpose: Convert bro JSON files to JSON TSV files

'''
import subprocess
import os,os.path
from glob import glob
from module.run_file import run_file
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
    """ gunzip all files in the input folder in case they are compressed """
    print("Being sure all files in %s are gunzipped" % (input_folder))
    p = subprocess.Popen("gunzip %s/*.gz" % (input_folder), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,)
    output, error = p.communicate()
    p_status = p.wait()
    print("Done gunzipping files in %s" % (input_folder))


def get_files_in_folder(input_folder):
    """ Return an array of files in the folder """
    files = []
    for abs_file_path in [y for x in os.walk(input_folder) for y in glob(os.path.join(x[0], '*'))]:
        path = "%s/" % ("/".join(map(str,(abs_file_path.split("/")[0:len(abs_file_path.split("/"))-1]))))
        file_name = abs_file_path.split("/")[len(abs_file_path.split("/")) - 1]
        files.append([path, file_name])   
    return files


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

    # Get an array of all of the files in the input folder
    files = get_files_in_folder(input_folder)

    # Run the files
    pbar = tqdm(total=len(files))
    def update(*a):
        pbar.update()
    for path, file_name in files:
        pool.apply_async(run_file, args=(path, file_name, output_folder, ), callback=update)

    # Keep running until everything is done
    pool.close()
    pool.join()
