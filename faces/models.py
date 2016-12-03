# -*- coding: utf-8 -*-
from django.db import models
import os

def user_directory_path(instance, filename):
    return 'documents/%s/%s'% (filename.split(".")[0], filename)

#the video file
class Document(models.Model):
    #the file
    docfile = models.FileField(upload_to=user_directory_path)
    #whether or not the file has been analyzed
    analyzed = models.BooleanField(default=False)
