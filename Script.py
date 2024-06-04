import os
import collections
from pprint import pprint

# Extensions for different file types
EXT_AUDIO = ['mp3', 'wav', 'raw', 'wma', 'mid', 'midi']
EXT_VIDEO = ['mp4', 'mpg', 'mpeg', 'avi', 'mov', 'flv', 'mkv', 'mwv', 'm4v', 'h264']
EXT_IMAGES  = ['png', 'jpg', 'jpeg', 'gif', 'svg', 'bmp', 'psd', 'svg', 'tiff', 'tif']
EXT_DOCS  = ['txt', 'pdf', 'csv', 'xls', 'xlsx', 'ods', 'doc', 'docx', 'html', 'odt', 'tex', 'ppt', 'pptx', 'log']
EXT_COMPRESSED = ['zip', 'z', '7z', 'rar', 'tar', 'gz', 'rpm', 'pkg', 'deb']
EXT_INSTLERS = ['dmg', 'exe', 'iso']

# Step 1 - Create the base directory on the Desktop
BASE_PATH = os.path.join(os.path.expanduser('~'), 'Desktop', 'Download_Sorted')
DEST_DIRS = ['Music', 'Movies', 'Pictures', 'Documents', 'Applications', 'Other', 'Compressed']

if not os.path.exists(BASE_PATH):
    os.mkdir(BASE_PATH)

for d in DEST_DIRS:
    dir_path = os.path.join(BASE_PATH, d)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

# Step 2 - Map files from Downloads folder based on their file extension 
DOWNLOADS_PATH = os.path.join(os.path.expanduser('~'), 'Downloads')
files_mapping = collections.defaultdict(list)
files_list = os.listdir(DOWNLOADS_PATH)

for file_name in files_list:
    if file_name[0] != '.' and os.path.isfile(os.path.join(DOWNLOADS_PATH, file_name)):
        file_ext = file_name.split('.')[-1].lower()
        files_mapping[file_ext].append(file_name)

pprint(files_mapping)

# Step 3 - Move all files given a file extension to a target directories in new created desktop folder
for f_ext, f_list in files_mapping.items():
    if f_ext in EXT_INSTLERS:
        target_dir = 'Applications'
    elif f_ext in EXT_AUDIO:
        target_dir = 'Music'
    elif f_ext in EXT_VIDEO:
        target_dir = 'Movies'
    elif f_ext in EXT_IMAGES:
        target_dir = 'Pictures'
    elif f_ext in EXT_DOCS:
        target_dir = 'Documents'
    elif f_ext in EXT_COMPRESSED:
        target_dir = 'Compressed'
    else:
        target_dir = 'Other'

    for file in f_list:
        src_path = os.path.join(DOWNLOADS_PATH, file)
        dest_path = os.path.join(BASE_PATH, target_dir, file)
        os.rename(src_path, dest_path)
