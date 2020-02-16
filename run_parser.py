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
parser.add_argument('-o', '--output_folder', required=True, help='output log folder')
parser.add_argument('-k', '--keep_original', required=False, action='store_true', help='keep the original gz files, deleting unpressed once converted')
args = parser.parse_args()
input_folder = args.input_folder
output_folder = args.output_folder


def gunzip_file(gz_file):
    """ gunzip all files in the input folder in case they are compressed """
    print("Uncompressing %s" % (gz_file))
    if args.keep_original:
        p = subprocess.Popen("gunzip %s --keep" % (gz_file), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,)
    else:
        p = subprocess.Popen("gunzip %s" % (gz_file), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,)
    output, error = p.communicate()
    p_status = p.wait()


def get_files_in_folder(input_folder):
    """ Return an array of files in the folder """
    files = []
    for abs_file_path in [y for x in os.walk(input_folder) for y in glob(os.path.join(x[0], '*'))]:
        path = "%s/" % ("/".join(map(str,(abs_file_path.split("/")[0:len(abs_file_path.split("/"))-1]))))
        file_name = abs_file_path.split("/")[len(abs_file_path.split("/")) - 1]
        files.append([path, file_name])   
    return files


if __name__ == "__main__":
    print('''
############################################################################################################
############################################################################################################
RITA NOW SUPPORTS JSON INPUT.  RECOMMEND THAT YOU USE THEIR NATIVE CAPABILITY INSTEAD OF JSON->TSV WITH THIS
############################################################################################################
############################################################################################################
    ''')    
    
    
    # Setup pool for processing the files
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    # Be sure base output folder folder is created
    try:
        os.mkdir(output_folder)
    except FileExistsError:
        pass

    # Get an array of all of the files in the input folder
    files = get_files_in_folder(input_folder)

    # Run the files
    print("Converting files from JSON to TSV")
    pbar = tqdm(total=len(files))
    def update(*a):
        pbar.update()
    for path, file_name in files:
        full_path_old = "%s/%s" % (path, file_name)
        while "//" in full_path_old:
            full_path_old = full_path_old.replace("//","/")

        full_path_new = "%s/%s" % (path, file_name)
        full_path_new = full_path_new.replace(input_folder, output_folder)
        while "//" in full_path_new:
            full_path_new = full_path_new.replace("//","/")

        if os.path.isdir(full_path_old):
            # In case there is a sub-directory, be sure the folder exists
            try:
                print("Making directory: %s" % (full_path_new))
                os.makedirs(full_path_new)
            except Exception as e:
                print("Error making directory: %s - %s" % (full_path_new, str(e)))
        else:
            # Be sure the file isn't compressed
            is_gz_file = False
            if ".gz" in full_path_old:
                is_gz_file = True
                gunzip_file(gz_file=full_path_old)
                full_path_old = full_path_old.replace(".gz","")
                full_path_new = full_path_new.replace(".gz","")

            #Run the file
            print("Running: %s" % (full_path_old))
            pool.apply_async(run_file, args=(full_path_old, full_path_new, is_gz_file), callback=update)

    # Keep running until everything is done
    pool.close()
    pool.join()
