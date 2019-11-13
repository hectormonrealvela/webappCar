from __future__ import unicode_literals
import string
import os
from django.db import models
from django.utils.timezone import now as timezone_now
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from model_utils import Choices


class Document(models.Model):

  user = models.CharField(User,max_length=200, null=True)
  Nombre = models.CharField(max_length=200, blank=True)
  document = models.FileField(upload_to='documents/')
  numb = models.IntegerField(null=True)
  uploaded_at = models.DateTimeField(auto_now_add=True)
  gps_northing = models.IntegerField(null=True,blank=True)
  gps_easting =  models.IntegerField(null=True,blank=True)
  layers = models.IntegerField(default=32)

  gps_lat = ArrayField(models.DecimalField(max_digits=10,decimal_places=3,), size=3, null=True,blank=True)
  gps_long = ArrayField(models.DecimalField(max_digits=10,decimal_places=3,), size=3, null=True,blank=True)






def upload_to(instance, filename):

    now = timezone_now()
    filename_base, filename_ext = os.path.splitext(filename)
    return format(
        filename_ext.lower())



class clasificador(models.Model):

    OBJETOS =Choices('Coche','Semáforo', 'Señal','Otros')

    objetos = models.CharField(choices=OBJETOS, max_length=20)
    nombre = models.CharField(max_length=200, null=True, blank=True)
    coordinatex = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    coordinatey = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    coordinatez = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    path = models.CharField(max_length=300, null=True, blank=True)









