Move Media
==========

Safely move photos and videos from a source directory with arbitrary files to
photo and video destination directories. The media type of the file is used to
determine if it's a photo or video. Any other media types are ignored.

The date and time the photo or video was taken is detected (if possible). If
it is a photo, the EXIF DateTimeOriginal tag is used if present. Else for
photos or videos, the date taken is inferred from the file name since most
media files are named by date taken. Finally, the modify time of the file is
used as a best guess. The destination files are organized by year and given a
consistent file name based on the detected date taken. If a destination file
with the same date taken and different checksum exists, an incrementing suffix
is appended to the file name.

You can optionally remove photos and videos from the source directory that are
older than a provided number of days. Files are only removed if the media file
is copied and matching checksum is verified or if the media file with matching
checksum already exists in the destination.

You can skip files that were recently modified within a provided number of
minutes.

My Use Case
-----------

I run this on my Dropbox camera uploads every night to:
  a. Free up space on Dropbox
  b. Point Plex at split up photos and videos directories
  c. Backup the organized photos and videos

Here's the crontab::

  # move dropbox camera uploads out of dropbox into media folders
  0 2 * * * mvmedia Dropbox/Camera\ Uploads --photos=Media/Pictures --videos=Media/Videos --remove=30 --recent=30 --verbose >> /var/log/dropbox/mvmedia.log

Usage
-----

Help::

  usage: mvmedia [-h] --photos PHOTOS --videos VIDEOS [--remove REMOVE]
                    [--recent RECENT] [--verbose]
                    source

  Move and rename photos and videos

  positional arguments:
    source           Source folder to read media from

  optional arguments:
    -h, --help       show this help message and exit
    --photos PHOTOS  Destination folder to move photos to
    --videos VIDEOS  Destination folder to move videos to
    --remove REMOVE  Remove files older than provided days
    --recent RECENT  Skip files recently modified within the provided minutes
    --verbose        Print verbose output
