"""
This file contains tests using the unittest module. These will pass
when you run "manage.py test".
"""

from django.test import TestCase

from filexplore.im_handler import *

class ImHandlerTest(TestCase):
    def test_image_filename_matching(self):
        """
        Tests that filenames for images are detected correctly
        """
        self.assertEqual(is_image_filename('abc.JPEG'), True)
        self.assertEqual(is_image_filename('abc.JPG'), True)
        self.assertEqual(is_image_filename('abc.jpeg'), True)
        self.assertEqual(is_image_filename('abc.jpg'), True)
        self.assertEqual(is_image_filename('abc.JPeg'), True)
        self.assertEqual(is_image_filename('abc.txt'), False)
        self.assertEqual(is_image_filename('abc.jpg.txt'), False)
