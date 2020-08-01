import logging
import re
import hashlib
import exifread

from pathlib import Path
from datetime import datetime


def get_date(path, is_image=False):
    # image EXIF date
    if is_image:
        with path.open('rb') as image:
            tags = exifread.process_file(image)

            if 'EXIF DateTimeOriginal' in tags:
                image_date = tags['EXIF DateTimeOriginal']
                split_date = [int(x) for x in re.sub(
                    r'[^0-9]', ' ', str(image_date)).split(' ')]

                logging.info('Using image {} EXIF date {}'
                             .format(path, image_date))

                return datetime(*split_date)

    # file name with YYYYMMDD HHMMSS or YYYY-MM-DD HH:MM:SS date
    file_name_date_match = re.search(
        r'(\d{4}).?(\d{2}).?(\d{2}).?(\d{2}).?(\d{2}).?(\d{2})', path.stem)

    if file_name_date_match:
        split_date = [int(x) for x in file_name_date_match.groups()]

        try:
            file_name_date = datetime(*split_date)

            logging.info('Using date format of file {} with date {}'
                         .format(path, file_name_date))

            return file_name_date
        except ValueError:
            logging.info('Matched date format of file {} is not a valid date'
                         .format(path))

    # modify time
    modify_date = get_modify_date(path)

    logging.info('Using file {} modify date {}'.format(path, modify_date))

    return modify_date


def get_modify_date(path):
    return datetime.fromtimestamp(path.stat().st_mtime)


def shasum_path(path):
    sha = hashlib.sha256()
    sha.update(path.read_bytes())

    return sha.digest()


def find_unique_path(path, shasum, count=1):
    incremented_path = path.with_name(
        '{}_{}{}'.format(path.stem, count, path.suffix))

    if incremented_path.exists():
        if shasum == shasum_path(incremented_path):
            return (incremented_path, False)

        return find_unique_path(path, shasum, count + 1)

    return (incremented_path, True)


def remove_old_path(path, keep_days=None):
    if keep_days is None:
        return

    path_modify_time = datetime.fromtimestamp(path.stat().st_mtime)
    time_since_path_modified = datetime.now() - path_modify_time

    if time_since_path_modified.days > keep_days:
        logging.info('Remove path {} that is older than {} days: last modified {} days ago'
                     .format(path, keep_days, time_since_path_modified.days))
        path.unlink()
        return True
