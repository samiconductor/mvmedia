import logging
import magic

from datetime import datetime, timedelta
from . import pathutil


def run(source_path, dest_photos_path, dest_videos_path, keep_old_path_days, skip_recent_modified_minutes):
    copied_count = 0
    already_copied_count = 0
    skip_recent_count = 0
    removed_count = 0
    shasum_mismatch_count = 0

    logging.info('--- Move Media ---')
    logging.info('Source: {}'.format(source_path))
    logging.info('Photos Destination: {}'.format(dest_photos_path))
    logging.info('Videos Destination: {}'.format(dest_videos_path))

    if skip_recent_modified_minutes is not None:
        logging.info('Skipping files modified less than {} minutes ago'
                     .format(skip_recent_modified_minutes))
    if keep_old_path_days is not None:
        logging.info('Removing copied files older than {} days'
                     .format(keep_old_path_days))

    for path in source_path.glob('**/*'):
        if not path.is_file():
            continue

        mime = magic.from_file(str(path), mime=True)
        image_mime = mime.startswith('image')
        video_mime = mime.startswith('video')
        media_mime = image_mime or video_mime

        if not media_mime:
            logging.warning('Skipping non-media file {}'.format(path))
            continue

        if skip_recent_modified_minutes is not None:
            modify_date = pathutil.get_modify_date(path)
            if datetime.now() - modify_date < timedelta(minutes=skip_recent_modified_minutes):
                logging.info('Skipping file modified less than {} minutes ago {}'
                             .format(skip_recent_modified_minutes, path))
                skip_recent_count += 1
                continue

        file_date = pathutil.get_date(path, is_image=image_mime)
        dest_path = dest_photos_path if image_mime else dest_videos_path
        date_path = dest_path / str(file_date.year)
        file_date_path = date_path / \
            '{}{}'.format(file_date.strftime('%Y-%m-%d %H-%M-%S'), path.suffix)

        if file_date_path.exists():
            source_shasum = pathutil.shasum_path(path)

            if source_shasum == pathutil.shasum_path(file_date_path):
                logging.info('Media file {} already copied to {}'
                             .format(path, file_date_path))
                already_copied_count += 1
                if pathutil.remove_old_path(path, keep_old_path_days):
                    removed_count += 1
                continue

            file_date_path, unique_found = pathutil.find_unique_path(
                file_date_path, source_shasum)

            if not unique_found:
                logging.info('Media file {} already copied to {}'
                             .format(path, file_date_path))
                already_copied_count += 1
                if pathutil.remove_old_path(path, keep_old_path_days):
                    removed_count += 1
                continue

        date_path.mkdir(parents=True, exist_ok=True)
        file_date_path.write_bytes(path.read_bytes())
        copied_count += 1

        logging.info('Media file {} copied to {}'.format(path, file_date_path))

        if pathutil.shasum_path(path) == pathutil.shasum_path(file_date_path):
            if pathutil.remove_old_path(path, keep_old_path_days):
                removed_count += 1
        else:
            logging.warning('Shasum of copied file {} and destination file {} do not match!'
                            .format(path, file_date_path))
            shasum_mismatch_count += 1

    logging.info('---Move Media Complete---')
    logging.info('Copied {} files'.format(copied_count))
    logging.info('Skipped {} files that were already copied'
                 .format(already_copied_count))

    if shasum_mismatch_count > 0:
        logging.info('There were {} copied shasum mismatches'
                     .format(shasum_mismatch_count))
    if skip_recent_modified_minutes is not None:
        logging.info('Skipped {} files that were modified less than {} minutes ago'
                     .format(skip_recent_count, skip_recent_modified_minutes))
    if keep_old_path_days is not None:
        logging.info('Removed {} files older than {} days'
                     .format(removed_count, keep_old_path_days))
