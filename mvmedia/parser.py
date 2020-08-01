import argparse


def parse():
    parser = argparse.ArgumentParser(
        description='Move and rename photos and videos')

    parser.add_argument('source',
                        help='Source folder to read media from')
    parser.add_argument('--photos', required=True,
                        help='Destination folder to move photos to')
    parser.add_argument('--videos', required=True,
                        help='Destination folder to move videos to')
    parser.add_argument('--remove', type=int,
                        help='Remove files older than provided days')
    parser.add_argument('--recent', type=int,
                        help='Skip files recently modified within the provided minutes')
    parser.add_argument('--verbose', action='store_true',
                        help='Print verbose output')

    return parser.parse_args()
