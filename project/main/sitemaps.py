from django.contrib.sitemaps import Sitemap
from blog.models import SummerNote
from django.urls import reverse


class SummerSitemap(Sitemap):

    def items(self):
        return SummerNote.objects.all()


class StaticViewSitemap(Sitemap):

    def items(self):
        return ['about']

    def location(self, obj):
        return reverse(obj)
