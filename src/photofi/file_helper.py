
from pathlib import Path as Path

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
