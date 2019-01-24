from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_summernote import models as summer_model
from django_summernote import fields as summer_fields

# Create your models here.


class HashTag(models.Model):
    title = models.CharField(blank=True, null=True, max_length=50)
    nou = models.IntegerField(blank=True, null=True, default=1)


# 메뉴 구분
class Classify(models.Model):
    title = models.CharField(blank=True, null=True, max_length=50)


class Category(models.Model):
    classify = models.ForeignKey(Classify, models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(blank=True, null=True, max_length=50)
    label = models.CharField(blank=True, null=True, max_length=50)
    nou = models.IntegerField(blank=True, null=True, default=1)
    use = models.CharField(blank=True, null=True, max_length=2, default='Y')


class SummerNote(summer_model.Attachment):
    index = models.IntegerField(blank=True, null=True)
    title = models.CharField(blank=True, null=True, max_length=50)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    summer_field = summer_fields.SummernoteTextField(default='')
    hits = models.IntegerField(blank=True, null=True, default=0)
    noc = models.IntegerField(blank=True, null=True, default=0)
    published_date = models.DateTimeField(blank=True, null=True)
    edited_date = models.DateTimeField(blank=True, null=True)
    hashtag = models.CharField(blank=True, null=True, max_length=500)
    tag1 = models.CharField(blank=True, null=True, max_length=50)
    tag2 = models.CharField(blank=True, null=True, max_length=50)
    tag3 = models.CharField(blank=True, null=True, max_length=50)
    tag4 = models.CharField(blank=True, null=True, max_length=50)
    tag5 = models.CharField(blank=True, null=True, max_length=50)

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])


class Comment(models.Model):
    post = models.ForeignKey(SummerNote, models.DO_NOTHING, blank=True, null=True)
    ip_display = models.CharField(max_length=16, null=False, default='')
    ip = models.CharField(max_length=16, null=False, default='')
    comment = models.CharField(max_length=150, null=False, default='')
    email = models.CharField(max_length=150, null=False, default='')
    author = models.CharField(max_length=9, null=False, default='')
    user = models.ForeignKey(User, default=None, null=True)
    password = models.CharField(max_length=300, null=False, default='')
    depth = models.IntegerField(null=True)
    parent = models.IntegerField(null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    delete = models.CharField(max_length=2, default='N')
    full_delete = models.CharField(max_length=2, default='N')


# 게시글 조회 기록 저장
class HitCount(models.Model):
    ip = models.CharField(max_length=15, default=None, null=True)  # ip 주소
    ip_display = models.CharField(max_length=16, null=False, default='')
    post = models.ForeignKey(SummerNote, default=None, null=True)  # 게시글
    date = models.DateField(default=None, null=True, blank=True)  # 조회수가 올라갔던 날짜
    number_of_get_request = models.IntegerField(default=0)  # 같은 날 GET 요청을 보낸 횟수
