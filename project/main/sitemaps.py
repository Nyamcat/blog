from django.contrib.sitemaps import Sitemap
from blog.models import SummerNote
from django.urls import reverse


class SummerSitemap(Sitemap):

    def items(self):
        return SummerNote.objects.filter(id__gte=2)


class StaticViewSitemap(Sitemap):

    def items(self):
        return ['guestbook', 'all_post']

    def location(self, obj):
        return reverse(obj)
