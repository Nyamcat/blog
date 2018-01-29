from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout
from . import views
from .views import IndexView, WriteView, BlogView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page' : '/'}, name='logout'),
    url(r'^blog/$', BlogView.as_view(), name='blog'),
    url(r'^blog/write/$', WriteView.as_view(), name='write'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

