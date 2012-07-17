import Image
import hashlib
import os
import re
from time import strptime, mktime
from datetime import datetime

from PIL.ExifTags import TAGS

from webxplore.models import Photo, Manufacturer, Camera

# Compute a hopefully unique hash based on path,
# used to save a thumbnail under.
def file_name_hash(path):
    return hashlib.sha224(path).hexdigest()

# Create and save a thumbnail
def make_thumbnail(im, outfile, size = (100, 100)):
    try:
        im.thumbnail(size)
        im.save(outfile)
    except IOError:
        return False
    return True

# Create a thumbnail and a database entry for the image
def import_image(path, thumb_path):
    # Check if it already exists
    try:
        ph = Photo.objects.get(path = path)
        return ph
    except Photo.DoesNotExist:
        # The photo is new, continue with importing
        pass

    # Compute file name for thumbnail
    outfile = os.path.join(thumb_path, file_name_hash(path) + ".jpg")

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

    # Save the thumbnail
    make_thumbnail(im, outfile)

    # Save to database
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
    )
    
    ph.save()

    return ph

# Check if a given filename is a file phoxplore can handle
def is_image_filename(filename):
    return re.search(r'.[Jj][Pp][Ee]?[Gg]$', filename) != None

# Give a list of images in given path and recursive subdirectories
def images_in_folder(path):
    all_files = []
    for root, dirs, files in os.walk(path):
        all_files += [os.path.join(root, f)
                        for f in files
                            if is_image_filename(f)]
    return all_files

# Import all images in a folder into phoxplore
def import_folder(path, thumb_path):
    images = []
    for impath in images_in_folder(path):
        images.append(
            import_image(impath, thumb_path)
        )

    return images