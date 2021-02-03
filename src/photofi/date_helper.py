import datetime

def set_creation_date_from_str(file: Path, str_datetime):
    try:
        # Turns out exif can have different formats - YYYY:MM:DD, YYYY/..., YYYY-... etc
        # God wish that americans won't have something like MM-DD-YYYY
        # The replace ': ' to ':0' fixes issues when it reads the string as 2006:11:09 10:54: 1.
        # It replaces the extra whitespace with a 0 for proper parsing
        str_datetime = str_datetime.replace('-', ':').replace('/', ':').replace('.', ':').replace('\\', ':').replace(': ', ':0')[:19]
        timestamp = _datetime.strptime(
            str_datetime,
            '%Y:%m:%d %H:%M:%S'
        ).timestamp()
        _os.utime(file, (timestamp, timestamp))
        if _os.name == 'nt':
            _windoza_setctime.setctime(str(file), timestamp)
    except Exception as e:
        print('Error setting creation date from string:')
        print(e)
        raise ValueError(f"Error setting creation date from string: {str_datetime}")

def set_creation_date_from_exif(file: Path):
    try:
        # Why do you need to be like that, Piexif...
        exif_dict = _piexif.load(str(file))
    except Exception as e:
        raise IOError("Can't read file's exif!")
    tags = [['0th', TAG_DATE_TIME], ['Exif', TAG_DATE_TIME_ORIGINAL], ['Exif', TAG_DATE_TIME_DIGITIZED]]
    datetime_str = ''
    date_set_success = False
    for tag in tags:
        try:
            datetime_str = exif_dict[tag[0]][tag[1]].decode('UTF-8')
            set_creation_date_from_str(file, datetime_str)
            date_set_success = True
            break
        except KeyError:
            pass  # No such tag - continue searching :/
        except ValueError:
            print("Wrong date format in exif!")
            print(datetime_str)
            print("does not match '%Y:%m:%d %H:%M:%S'")
    if not date_set_success:
        raise IOError('No correct DateTime in given exif')

def set_file_exif_date(file: Path, creation_date):
    try:
        exif_dict = _piexif.load(str(file))
    except:  # Sorry but Piexif is too unpredictable
        exif_dict = {'0th': {}, 'Exif': {}}

    creation_date = creation_date.encode('UTF-8')
    exif_dict['0th'][TAG_DATE_TIME] = creation_date
    exif_dict['Exif'][TAG_DATE_TIME_ORIGINAL] = creation_date
    exif_dict['Exif'][TAG_DATE_TIME_DIGITIZED] = creation_date

    try:
        _piexif.insert(_piexif.dump(exif_dict), str(file))
    except Exception as e:
        print("Couldn't insert exif!")
        print(e)
        nonlocal s_cant_insert_exif_files
        s_cant_insert_exif_files.append(str(file.resolve()))
