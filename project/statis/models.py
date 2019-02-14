from django.db import models

# Create your models here.


class Visitor(models.Model):
    ip = models.CharField(max_length=15, default=None, null=True)  # ip 주소
    ip_display = models.CharField(max_length=16, null=False, default='')
    date = models.DateField(default=None, null=True, blank=True)  # 방문자 수가 올라갔던 날짜
    number_of_get_request = models.IntegerField(default=0)  # 같은 날 GET 요청을 보낸 횟수


class VisitorTotal(models.Model):
    cnt = models.IntegerField(default=0, null=True, blank=True)
