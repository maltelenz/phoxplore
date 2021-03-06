import Image
import os
from time import strptime, mktime
from datetime import datetime

from ExifTags import TAGS

from django.conf import settings

from webxplore.models import Photo, Manufacturer, Camera, SourceFolder

from filexplore.file_handler import *

# Create and save an image of given size
def save_resized(im, outfile, size = (200, 200)):
    try:
        imcopy = im.copy()
        imcopy.thumbnail(size, Image.ANTIALIAS)
        imcopy.save(outfile, quality = 95)
    except IOError:
        return False
    return True

# Create a thumbnail and a database entry for the image
def import_image(path, source_folder, thumb_path = settings.THUMBNAIL_DIR):
    # Check if it already exists
    try:
        ph = Photo.objects.get(path = path)
        return ph
    except Photo.DoesNotExist:
        # The photo is new, continue with importing
        pass

    # Collect various data about the image
    im = Image.open(path)
    (width, height) = im.size
    exif_raw = im._getexif()
    exif_parsed = {}
    for tag, value in exif_raw.items():
        decoded = TAGS.get(tag, tag)
        exif_parsed[decoded] = value

    (exposure_numerator, exposure_denominator) = exif_parsed['ExposureTime']

    # It is assumed that django will change this
    # into the time zone set in settings.
    taken_date = datetime.fromtimestamp(mktime(
        strptime(
            exif_parsed['DateTimeOriginal'],
            "%Y:%m:%d %H:%M:%S"
        )
    ))

    file_size = os.stat(path).st_size

    manufacturer_name = exif_parsed['Make']
    camera_name = exif_parsed['Model']

    manufacturer, created = Manufacturer.objects.get_or_create(
        name = manufacturer_name
    )
    camera, created = Camera.objects.get_or_create(
        manufacturer = manufacturer,
        name = camera_name
    )

    focal_length = exif_parsed['FocalLength'][0]

    aperture = exif_parsed['FNumber'][0]

    iso = exif_parsed['ISOSpeedRatings']

    # Compute file name for large size
    largefile = os.path.join(thumb_path, large_sub_path(path))

    # Save large view size
    save_resized(im, largefile, (1000, 1000))

    # Compute file name for medium size
    mediumfile = os.path.join(thumb_path, medium_sub_path(path))

    # Save medium view size
    save_resized(im, mediumfile, (600, 600))

    # Compute file name for thumbnail
    thumbfile = os.path.join(thumb_path, thumb_sub_path(path))

    # Save thumbnail
    save_resized(im, thumbfile)

    # Save to database
    ph = Photo(
        path = path,
        source_folder = source_folder,
        width = width,
        height = height,
        exposure_numerator = exposure_numerator,
        exposure_denominator = exposure_denominator,
        iso = iso,
        taken_date = taken_date,
        file_size = file_size,
        camera = camera,
        focal_length = focal_length,
        aperture = aperture
    )

    ph.save()

    return ph


# Import all images in a folder into phoxplore
def import_folder(path, name = None, thumb_path = settings.THUMBNAIL_DIR):
    images = []

    if name is None:
        name = path

    source_folder = SourceFolder(path = path, name = name)

    source_folder.save()

    for impath in images_in_folder(path):
        images.append(
            import_image(impath, source_folder, thumb_path)
        )

    return images