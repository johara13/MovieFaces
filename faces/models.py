# -*- coding: utf-8 -*-
from django.db import models
import os

def user_directory_path(instance, filename):
    return 'documents/%s/%s'% (filename.split(".")[0], filename)

class Document(models.Model):
    docfile = models.FileField(upload_to=user_directory_path)
    analyzed = models.BooleanField(default=False)
