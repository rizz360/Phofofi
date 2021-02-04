
from pathlib import Path as Path
import hashlib as _hashlib

# File definitions
photo_formats = ['.jpg', '.jpeg', '.png', '.webp',
                 '.bmp', '.tif', '.tiff', '.svg', '.heic']
video_formats = ['.mp4', '.gif', '.mov', '.webm', '.avi', '.wmv',
                 '.rm', '.mpg', '.mpe', '.mpeg', '.mkv', '.m4v', '.mts', '.m2ts']

# holds all the renamed files that clashed from their
rename_map = dict()

def for_all_files_recursive(
    dir: Path,
    file_function=lambda fi: True,
    folder_function=lambda fo: True,
    filter_fun=lambda file: True
):
    for file in dir.rglob("*"):
        if file.is_dir():
            folder_function(file)
            continue
        elif file.is_file():
            if filter_fun(file):
                file_function(file)
        else:
            print('Found something weird...')
            print(file)


def is_photo(file: Path):
    if file.suffix.lower() not in photo_formats:
        return False
    return True


def is_video(file: Path):
    if file.suffix.lower() not in video_formats:
        return False
    return True


def chunk_reader(fobj, chunk_size=1024):
    """ Generator that reads a file in chunks of bytes """
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk


def get_hash(file: Path, first_chunk_only=False, hash_algo=_hashlib.sha1):
    hashobj = hash_algo()
    with open(file, "rb") as f:
        if first_chunk_only:
            hashobj.update(f.read(1024))
        else:
            for chunk in chunk_reader(f):
                hashobj.update(chunk)
    return hashobj.digest()

# Makes a new name like 'photo(1).jpg'
def new_name_if_exists(file: Path):
    new_name = file
    i = 1
    while True:
        if not new_name.is_file():
            return new_name
        else:
            new_name = file.with_name(f"{file.stem}({i}){file.suffix}")
            rename_map[str(file)] = new_name
            i += 1
