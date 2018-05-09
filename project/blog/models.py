from django.db import models
from django_summernote import models as summer_model
from django_summernote import fields as summer_fields

# Create your models here.


class SummerNote(summer_model.Attachment):
    title = models.CharField(blank=True, null=True, max_length=50)
    summer_field = summer_fields.SummernoteTextField(default='')
    hits = models.IntegerField(blank=True, null=True, default=0)
    published_date = models.DateTimeField(blank=True, null=True)
    edited_date = models.DateTimeField(blank=True, null=True)
    tag1 = models.CharField(blank=True, null=True, max_length=50)
    tag2 = models.CharField(blank=True, null=True, max_length=50)
    tag3 = models.CharField(blank=True, null=True, max_length=50)
    tag4 = models.CharField(blank=True, null=True, max_length=50)
    tag5 = models.CharField(blank=True, null=True, max_length=50)



class HashTag(models.Model):
    title = models.CharField(blank=True, null=True, max_length=50)
    nou = models.IntegerField(blank=True, null=True, default=1)