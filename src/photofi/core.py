
from photofi import file_helper
from photofi import date_helper

_logger = logging.getLogger(__name__)

# Variables
## Statistics:
s_removed_duplicates_count = 0
s_folders_created = 0
s_files_moved = 0
s_files_fixed = 0

## File definitions
photo_formats = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tif', '.tiff', '.svg', '.heic']
video_formats = ['.mp4', '.gif', '.mov', '.webm', '.avi', '.wmv', '.rm', '.mpg', '.mpe', '.mpeg', '.mkv', '.m4v', '.mts', '.m2ts']

def main(args):
    INPUT_DIR = Path(args.input_folder)
    OUTPUT_DIR = Path(args.output_folder)

    _logger.info(INPUT_DIR)
    _logger.info(OUTPUT_DIR)

    # First we'll fix the metadata
    if args.fix-meta-data:
        _logger.info('Fixing meta data')
        for_all_files_recursive(
            dir=PHOTOS_DIR,
            file_function=fix_metadata,
            filter_fun=lambda f: (is_photo(f) or is_video(f))
        )

    # Removing duplicates - Some options here
    #   - Run through all the files again, this time checking-for and removing duplicates
    #   - While copying/moving the photos decide which one to keep and deleting the old one (or putting it in a seperate folder)

    # Moving (or copying) all the files into the appropriate folder
    for_all_files_recursive(
            dir=PHOTOS_DIR,
            file_function=copy_to_target_and_divide,
            filter_fun=lambda f: (is_photo(f) or is_video(f))
    )

    




def fix_metadata(file: Path):
    print(file)

    has_nice_date = False
    try:
        set_creation_date_from_exif(file)
        has_nice_date = True
    except (_piexif.InvalidImageDataError, ValueError, IOError) as e:
        print(e)
        print(f'No exif for {file}')
    except IOError:
        print('No creation date found in exif!')

    try:
        google_json = find_json_for_file(file)
        date = get_date_str_from_json(google_json)
        set_file_geo_data(file, google_json)
        set_file_exif_date(file, date)
        set_creation_date_from_str(file, date)
        has_nice_date = True
        return
    except FileNotFoundError:
        print("Couldn't find json for file ")

    if has_nice_date:
        return True

    print('Last chance, copying folder meta as date...')
    date = get_date_from_folder_meta(file.parent)
    if date is not None:
        set_file_exif_date(file, date)
        set_creation_date_from_str(file, date)
        nonlocal s_date_from_folder_files
        s_date_from_folder_files.append(str(file.resolve()))
        return True
    else:
        print('WARNING! There was literally no option to set date!!!')
        nonlocal s_no_date_at_all
        s_no_date_at_all.append(str(file.resolve()))

    return False

def copy_to_target(file: Path):
    if is_photo(file) or is_video(file):
        new_file = new_name_if_exists(FIXED_DIR / file.name)
        _shutil.copy2(file, new_file)
        nonlocal s_copied_files
        s_copied_files += 1
    return True
# Example: Photos from 2021/02/IMG_1234.JPG
def copy_to_target_and_divide(file: Path):
    creation_date = file.stat().st_mtime
    date = _datetime.fromtimestamp(creation_date)

    new_path = FIXED_DIR / f"{date.year}/{date.month:02}/"
    new_path.mkdir(parents=True, exist_ok=True)

    new_file = new_name_if_exists(new_path / file.name)
    _shutil.copy2(file, new_file)
    nonlocal s_copied_files
    s_copied_files += 1
    return True
