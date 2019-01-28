from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout, password_change
from django.contrib.sitemaps.views import sitemap

from . import views
from .views import IndexView, AboutView, SignupView, ProfileView
from .sitemaps import SummerSitemap, StaticViewSitemap

sitemaps= {
    'static': StaticViewSitemap,
    'posts' : SummerSitemap
}


urlpatterns = [
    url(r'^test/$', IndexView.as_view(), name='index'),
    url(r'^about', AboutView.as_view(), name='about'),
    url(r'^sitemap.xml$', sitemap, {'sitemaps': sitemaps}),

    # regist
    url(r'^accounts/login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page' : '/'}, name='logout'),
    url(r'^accounts/signup/$', SignupView.as_view(), name='signup'),
    url(r'^accounts/profile/$', ProfileView.as_view(), name='profile'),
    url(r'^accounts/password/$', password_change, {'post_change_redirect': '/', 'template_name':
                                                   'registration/password_change.html'}, name='password_change'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
