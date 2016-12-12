# -*- coding: utf-8 -*-
from django.db import models
import os

def user_directory_path(instance, filename):
    return 'documents/%s/%s'% (filename.split(".")[0], filename)

#the video file
class Document(models.Model):
    docfile = models.FileField(upload_to=user_directory_path)
    analyzed = models.BooleanField(default=False)
    v_scoreHappy = models.IntegerField(default=0)
    v_scoreSad = models.IntegerField(default=0)
    v_scoreAngry = models.IntegerField(default=0)
    v_scoreSurprise = models.IntegerField(default=0)

    def __str__(self):
        return self.docfile.url

class Picture(models.Model):
    video_loc = models.ForeignKey(Document, on_delete=models.CASCADE)
    picfile = models.FileField()
    analyzed = models.BooleanField(default=False)
    #the emotion each face has if it has one
    numFaces = models.IntegerField(default=0)
    face1 = models.CharField(max_length=200, null=True, blank=True)
    face2 = models.CharField(max_length=200, null=True, blank=True)
    face3 = models.CharField(max_length=200, null=True, blank=True)
    face4 = models.CharField(max_length=200, null=True, blank=True)
    hasFace = models.BooleanField(default=False)

