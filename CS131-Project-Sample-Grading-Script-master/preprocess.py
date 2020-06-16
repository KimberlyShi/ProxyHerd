import tarfile
from zipfile import ZipFile
import shutil
import os
import sys
import pandas as pd
import re

submissions_dir = "./sample_submission/"
project_code_fname = ["project.tgz", "project.tar.gz", "report.tgz", "server.tgz", "project.zip"]
project_file_fname = "server.py"
allowed_names = ['Hill', 'Jaquez', 'Smith', 'Campbell', 'Singleton']

def extract_tgzfile(fdir, fname_raw):
    fname = os.path.join(fdir, fname_raw)
    if not os.path.exists(fname):
        return False
    tar = tarfile.open(fname, "r:gz")
    tar.extractall(path=fdir) # without path being specified, it'll be extracted to the current repository
    tar.close()
    return True

def extract_tarfile(fdir, fname_raw):
    fname = os.path.join(fdir, fname_raw)
    if not os.path.exists(fname):
        return False
    tar = tarfile.open(fname, "r:")
    tar.extractall(path=fdir)
    tar.close()
    return True

def extract_zip(fdir, fname_raw):
    fname = os.path.join(fdir, fname_raw)
    if not os.path.exists(fname):
        return False
    with ZipFile(fname, 'r') as zipObj:
        # Extract all the contents of zip file in current directory
        zipObj.extractall(path=fdir)
    return True

def extract(fdir, fname_raw):
    success = False
    try:
        success = extract_tgzfile(fdir, fname_raw)
    except:
        try:
            success = extract_zip(fdir, fname_raw)
        except:
            try:
                success = extract_tarfile(fdir, fname_raw)
            except:
                print("tried all approaches for {} but all not working".format(os.path.join(fdir, fname_raw)))
    return success

def extract_files():
    fdir = submissions_dir
    if os.path.exists(os.path.join(fdir, project_file_fname)):
        # it is submitted as files, unzipped
        print("already unzipped")
        return True
    success = False
    for fname in project_code_fname:
        try:
            success = extract(fdir, fname)
            if success:
                os.remove(os.path.join(fdir, fname))
                break
        except:
            continue
            # continue trying other file names
    if not success:
        print("there's something wrong with preprocessing your submission file")
    else:
        subdir = None
        for root, subdirs, files in os.walk(fdir): # it lists everything recursively this way
            if len(subdirs) == 0:
                # no subdirectories
                break
            subdir = os.path.join(fdir, subdirs[0])
            for code_file in os.listdir(subdir):
                shutil.move(os.path.join(subdir, code_file), os.path.join(fdir, code_file))
    return False

def check_server_valid():
    '''check if all server.py are valid'''
    server_file = os.path.join(submissions_dir, project_file_fname)
    if not os.path.exists(server_file):
        print("not exists server.py")

def check_reports_valid():
    '''check if all reports are valid'''
    for root, subdirs, files in os.walk(submissions_dir):
        report_file = [os.path.join(submissions_dir, f) for f in files if f.endswith(".pdf") or f.endswith(".PDF")]
        break
    if len(report_file) == 0:
        print("not exists report")

if __name__ == '__main__':
    
    confirm_unzipped = extract_files()
    if not confirm_unzipped:
        extract_files() # we have to do this again because some students are submitting zipped zip...

    check_server_valid()
    check_reports_valid()

