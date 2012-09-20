import os

from django.db import models
from django.conf import settings
from filexplore.file_handler import *

class Manufacturer(models.Model):
    name = models.CharField(max_length = 500)
    
    class Meta:
        verbose_name = 'Manufacturer'
        verbose_name_plural = 'Manufacturers'

    def __unicode__(self):
        return self.name
    

class Camera(models.Model):
    manufacturer = models.ForeignKey(Manufacturer)
    name = models.CharField(max_length = 500)

    class Meta:
        verbose_name = 'Camera'
        verbose_name_plural = 'Cameras'

    def __unicode__(self):
        return self.manufacturer + ": " + self.name
    

class SourceFolder(models.Model):
    path = models.CharField(max_length = 10000)
    name = models.CharField(max_length = 200)

    class Meta:
        verbose_name = 'Source folder'
        verbose_name_plural = 'Source folders'

    def __unicode__(self):
        return self.name + " -> " + self.path


class Photo(models.Model):
    path = models.CharField(max_length = 10000)
    source_folder = models.ForeignKey(SourceFolder)
    width = models.IntegerField()
    height = models.IntegerField()
    exposure_numerator = models.IntegerField('Exposure numerator')
    exposure_denominator = models.IntegerField('Exposure denominator')
    iso = models.IntegerField('ISO speed')
    taken_date = models.DateTimeField()
    file_size = models.IntegerField('File size in bytes')
    camera = models.ForeignKey(Camera)
    focal_length = models.IntegerField()
    aperture = models.FloatField()

    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    def __unicode__(self):
        return self.path

    def thumb_path(self):
        return settings.MEDIA_URL + thumb_sub_path(self.path)

    def medium_path(self):
        return settings.MEDIA_URL + medium_sub_path(self.path)

    def large_path(self):
        return settings.MEDIA_URL + large_sub_path(self.path)

    def file_name(self):
        return os.path.basename(self.path)

    def exposure(self):
        return unicode(self.exposure_numerator) + "/" + unicode(self.exposure_denominator)

