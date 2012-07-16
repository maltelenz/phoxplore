from django.db import models

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
    

class Photo(models.Model):
    ORIENTATION_CHOICES = (
        ('LS','Landscape'),
        ('PT','Portrait'),
    )
    
    path = models.CharField(max_length = 10000)
    width = models.IntegerField()
    height = models.IntegerField()
    exposure = models.IntegerField('Exposure in microseconds')
    iso = models.IntegerField('ISO speed')
    orientation = models.CharField(max_length = 2, choices = ORIENTATION_CHOICES)
    taken_date = models.DateTimeField()
    fileSize = models.IntegerField('File size in bytes')
    camera = models.ForeignKey(Camera)
    focal_length = models.IntegerField()

    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    def __unicode__(self):
        return self.path


class SourceFolder(models.Model):
    path = models.CharField(max_length = 10000)

    class Meta:
        verbose_name = 'Source folder'
        verbose_name_plural = 'Source folders'

    def __unicode__(self):
        return self.path

