import hashlib
import os
import re

# Compute a hopefully unique hash based on path,
# used to save a thumbnail under.
def file_name_hash(path):
    return hashlib.sha224(path).hexdigest()


# Construct part of a path for different view size thumbnails
def thumb_sub_path(path):
    return os.path.join('thumb', file_name_hash(path) + ".jpg")


def medium_sub_path(path):
    return os.path.join('medium', file_name_hash(path) + ".jpg")


def large_sub_path(path):
    return os.path.join('large', file_name_hash(path) + ".jpg")


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
