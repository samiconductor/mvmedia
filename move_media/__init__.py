import logging
import sys

from pathlib import Path
from . import parser
from . import move


def ensure_path_exists(path):
    if not path.exists():
        print('The path {} does not exist!'.format(path), file=sys.stderr)
        exit(1)


def main():
    args = parser.parse()

    source_path = Path(args.source)
    dest_photos_path = Path(args.photos)
    dest_videos_path = Path(args.videos)
    keep_old_path_days = args.remove
    skip_recent_modified_minutes = args.recent
    verbose = args.verbose

    logging_level = logging.INFO if args.verbose else logging.ERROR
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                        level=logging_level, stream=sys.stdout)

    ensure_path_exists(source_path)
    ensure_path_exists(dest_photos_path)
    ensure_path_exists(dest_videos_path)

    move.run(
        source_path,
        dest_photos_path,
        dest_videos_path,
        keep_old_path_days,
        skip_recent_modified_minutes
    )
