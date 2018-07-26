from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout
from django.contrib.sitemaps.views import sitemap

from . import views
from .views import IndexView, AboutView
from .sitemaps import SummerSitemap, StaticViewSitemap

sitemaps= {
    'posts' : SummerSitemap,
    'static': StaticViewSitemap
}


urlpatterns = [
    url(r'^test/^$', IndexView.as_view(), name='index'),
    url(r'^about', AboutView.as_view(), name='about'),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^sitemap.xml$', sitemap, {'sitemaps': sitemaps}),
    url(r'^logout/$', logout, {'next_page' : '/'}, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

