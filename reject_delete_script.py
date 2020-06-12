import os

ACCEPTABLE_EXTENSIONS = ['raf', 'arw']

_dir = os.getcwd()
_ref_files = []
_ref_files_paths = []

def _getRefFilesFromDir(dir):
  _dir = dir
  for root, subdirs, files in os.walk(_dir):
    for f in files:
      _split = f.split('.')
      _extension = _split[len(_split) - 1].lower()
      _split.pop()
      _name = '.'.join(_split)
      if (_extension in ACCEPTABLE_EXTENSIONS):
        _ref_files.append(_name)
        _ref_files_paths.append(os.path.join(root, f))

def _getTargetDir():
  _target = input("Type in the target destination for files to be deleted: ")
  # _target = "C:\\Users\\chong\\Documents\\Japanese"
  while (not os.path.isdir(_target)):
    print("Please enter a valid path.")
    _target = input("Type in the target destination for files to be deleted: ")
  print('Target directory: ' + _target)
  _scanMatchingFiles(_target)

def _scanMatchingFiles(target):
  _target_files = []
  _target = target
  for root, subdirs, files in os.walk(_target):
    for f in files:
      _split = f.split('.')
      _extension = _split[len(_split) - 1].lower()
      _split.pop()
      _name = '.'.join(_split)
      if (_name in _ref_files and (_extension == "jpg" or _extension == "jpeg")):
        _path = os.path.join(root, f)
        _target_files.append(os.path.join(root, f))
  _getConfirmation(_target_files)

def _deleteFiles(arr):
  for f in arr:
    os.remove(f)

def _getConfirmation(target_files):
  _target_files = target_files
  for f in _target_files:
    print(f)
  _confirmation = input("The above files will be deleted. Continue? ({}) (y/n): ".format(len(_target_files)))
  while not _confirmation in ['y','n']:
    _confirmation = input("The above files will be deleted. Continue? ({}) (y/n): ".format(len(_target_files)))
  if _confirmation == 'y':
   _deleteFiles(_target_files)
  else:
    exit

def _alsoDeleteCurrentFiles():
  _confirmation = input("Also delete source folder files? (y/n): ")
  while not _confirmation in ['y','n']:
    _confirmation = input("Also delete source folder files? (y/n): ")
  if _confirmation == 'y':
   _getConfirmation(_ref_files_paths)
  else:
    exit

print("This program deletes any files in the given target directory (and sub-directories) matching the names of any file in the present directory with extensions: " + ', '.join(ACCEPTABLE_EXTENSIONS))
_getRefFilesFromDir(_dir)
_getTargetDir()
_alsoDeleteCurrentFiles()

