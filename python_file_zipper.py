import os
import py7zr
from time import time
from datetime import timedelta
from multiprocessing import Pool
import math

ACCEPTABLE_EXTENSIONS = ['raf', 'arw', 'jpg', 'jpeg']

_files_processed = 0
_total = 1

def getFilesFromDir(directory):
    _files = []
    _dir = directory
    for root, subdirs, files in os.walk(_dir):
        for f in files:
            _split = f.split('.')
            _extension = _split[len(_split) - 1].lower()
            _split.pop()
            _name = '.'.join(_split)
            if (_extension in ACCEPTABLE_EXTENSIONS):
                _files.append(os.path.join(root, f))
    return _files


def getTargetDirectory(msg):
    _target = input(msg)
    if (_target == ""):
        return os.getcwd()
    while (not os.path.isdir(_target)):
        print("Please enter a valid path.")
        _target = input(msg)
    return _target


def archiveFile(args):
    input = args[0]
    output = args[1]
    _archive = py7zr.SevenZipFile(output, 'w')
    _archive.writeall(input)
    _archive.close()
    # updatePercentage(output)

def updatePercentage(filename):
    global _files_processed
    global _total

    _files_processed += 1
    _percentage_completion = round(_files_processed/_total * 100, 2)
    print("Zipped {0} ({1}%)".format(filename, _percentage_completion))

def archiveAllIndividually(files, input_dir, output_dir):
    global _files_processed
    global _total
    _input_base = os.path.basename(input_dir)
    _total = len(files)
    _files_processed = 0
    _jobs = [];
    for f in files:
        _input = f
        _rel_path = os.path.relpath(f, input_dir)
        _rel_path = os.path.join(_input_base, _rel_path)
        _output_base = os.path.join(output_dir, _rel_path)
        _output = _output_base + ".7z"
        _output_dir = os.path.dirname(_output)
        if not os.path.exists(_output_dir):
            os.makedirs(_output_dir)
        counter = 1
        while os.path.exists(_output):
            _output = _output_base + "_" + str(counter) + ".7z"
            counter += 1
        _jobs.append([_input, _output])
    
    print("Using " + str(os.cpu_count()) + " cores.")
    with Pool() as p:
        p.map(archiveFile, _jobs)


def getConfirmation(target_files):
    _target_files = target_files
    for f in _target_files:
        print(f)
    _confirmation = input(
        "The above files will be archived. Continue? ({}) (y/n): ".format(len(_target_files)))
    while not _confirmation in ['y', 'n']:
        _confirmation = input(
            "The above files will be archived. Continue? ({}) (y/n): ".format(len(_target_files)))
    if _confirmation == 'y':
        return True
    else:
        return False


if __name__ == "__main__":
    currtime = time()
    _input_msg = "Enter the root directory to be archived (leave blank to select the current directory): "
    _output_msg = "Enter the target directory for the archived files (leave blank to select the current directory): "
    _input_dir = getTargetDirectory(_input_msg)
    _input_files = getFilesFromDir(_input_dir)
    _output_dir = getTargetDirectory(_output_msg)
    if (getConfirmation(_input_files)):
        archiveAllIndividually(_input_files, _input_dir, _output_dir)
    print("time taken: " + str(timedelta(seconds=time() - currtime)))
    print("average time per file: " + str((time() - currtime) / _total) + " s")
