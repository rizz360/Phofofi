
from photofi import file_helper
from photofi import date_helper

from pathlib import Path as Path
import shutil as _shutil
import piexif as _piexif
from datetime import datetime as _datetime

import logging
_logger = logging.getLogger(__name__)

# Variables
# Statistics:
s_removed_duplicates_count = 0
s_folders_created = 0
s_files_moved = 0
s_files_fixed = 0

s_removed_duplicates_count = 0
s_copied_files = 0
s_date_from_folder_files = []  # List of files where date was set from folder name
s_skipped_extra_files = []  # List of extra files ("-edited" etc) which were skipped
s_no_json_found = []  # List of files where we couldn't find json
s_no_date_at_all = []  # List of files where there was absolutely no option to set correct date

INPUT_DIR = ""
OUTPUT_DIR = ""


def main(args):
    """Main entry point allowing external calls
    Args:
      args ([str]): command line parameter list
    """

    INPUT_DIR = Path(args.input_folder)
    OUTPUT_DIR = Path(args.output_folder)

    _logger.info(INPUT_DIR)
    _logger.info(OUTPUT_DIR)

    # First we'll fix the metadata
    if args.fix_meta_data:
        _logger.info('Fixing meta data')
        file_helper.for_all_files_recursive(
            dir=INPUT_DIR,
            file_function=fix_metadata,
            filter_fun=lambda f: (file_helper.is_photo(f) or file_helper.is_video(f))
        )

    # Removing duplicates - Some options here
    #   - Run through all the files again, this time checking-for and removing duplicates
    #   - While copying/moving the photos decide which one to keep and deleting the old one (or putting it in a seperate folder)

    # Moving (or copying) all the files into the appropriate folder
    file_helper.for_all_files_recursive(
        dir=INPUT_DIR,
        file_function=move_to_target_and_divide,
        filter_fun=lambda f: (file_helper.is_photo(f) or file_helper.is_video(f))
    )


def fix_metadata(file: Path):
    print(file)

    has_nice_date = False
    try:
        date_helper.set_creation_date_from_exif(file)
        has_nice_date = True
    except (_piexif.InvalidImageDataError, ValueError, IOError) as e:
        print(e)
        print(f'No exif for {file}')
    except IOError:
        print('No creation date found in exif!')

    if has_nice_date:
        return True

    print('WARNING! There was literally no option to set date!!!')
    s_no_date_at_all.append(str(file.resolve()))

    return False


def move_to_target_and_divide(file: Path):
    creation_date = file.stat().st_mtime
    date = _datetime.fromtimestamp(creation_date)

    new_path = OUTPUT_DIR / f"{date.year}/{date.month:02}/"
    new_path.mkdir(parents=True, exist_ok=True)

    new_file = file_helper.new_name_if_exists(new_path / file.name)
    # Check for duplicates here

    _shutil.move(file, new_file)
    s_files_moved += 1
    return True
