import os
import py7zr

ACCEPTABLE_EXTENSIONS = ['raf', 'arw', 'jpg', 'jpeg']

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

def archiveFile(input, output):
    _archive = py7zr.SevenZipFile(output, 'w')
    _archive.writeall(input)
    _archive.close()

def archiveAllIndividually(files, input_dir, output_dir):
    _input_base = os.path.basename(input_dir)
    _total = len(files)
    _files_processed = 0
    for f in files:
        _files_processed += 1
        _percentage_completion = round(_files_processed/_total * 100, 2)
        _input = f
        _rel_path = os.path.relpath(f, input_dir)
        _rel_path = os.path.join(_input_base, _rel_path)
        _output_base = os.path.join(output_dir, _rel_path)
        # _output_split = _output_with_extension.split('.')
        # _output_split.pop()
        # _output_base = ".".join(_output_split) 
        _output = _output_base + ".7z"
        _output_dir = os.path.dirname(_output)
        if not os.path.exists(_output_dir):
            os.makedirs(_output_dir)
        counter = 1
        while os.path.exists(_output):
            _output = _output_base + "_" + str(counter) + ".7z"
            counter += 1
        print("Zipped {0} ({1}%)".format(_output, _percentage_completion))
        archiveFile(_input, _output)

def getConfirmation(target_files):
  _target_files = target_files
  for f in _target_files:
    print(f)
  _confirmation = input("The above files will be archived. Continue? ({}) (y/n): ".format(len(_target_files)))
  while not _confirmation in ['y','n']:
    _confirmation = input("The above files will be archived. Continue? ({}) (y/n): ".format(len(_target_files)))
  if _confirmation == 'y':
      return True
  else:
    return False

_input_msg = "Enter the root directory to be archived (leave blank to select the current directory): "
_output_msg = "Enter the target directory for the archived files (leave blank to select the current directory): "
print(os.path.basename(os.getcwd()))
_input_dir = getTargetDirectory(_input_msg)
_input_files = getFilesFromDir(_input_dir)
_output_dir = getTargetDirectory(_output_msg)
if (getConfirmation(_input_files)): 
    archiveAllIndividually(_input_files, _input_dir, _output_dir)
