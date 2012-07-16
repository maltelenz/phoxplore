import Image
import hashlib
import os
from time import strptime, mktime
from datetime import datetime

from PIL.ExifTags import TAGS

from webxplore.models import Photo, Manufacturer, Camera

def file_name_hash(path):
    return hashlib.sha224(path).hexdigest()

def make_thumbnail(im, outfile, size = (100, 100)):
    try:
        im.thumbnail(size)
        im.save(outfile)
    except IOError:
        return False
    return True

def import_image(path, thumb_path):
    outfile = os.path.join(thumb_path, file_name_hash(path) + ".jpg")
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

    manufacturer, created = Manufacturer.objects.get_or_create(name = manufacturer_name)
    camera, created = Camera.objects.get_or_create(manufacturer = manufacturer, name = camera_name)

    focal_length = exif_parsed['FocalLength'][0]

    aperture = exif_parsed['FNumber'][0]

    iso = exif_parsed['ISOSpeedRatings']

    make_thumbnail(im, outfile)

    ph = Photo(
        path = path,
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
        ).save()
    
    return ph
