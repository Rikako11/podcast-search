from django.urls import path
from django.conf.urls import url

from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url


urlpatterns = [
    path('', views.index, name='index'),
    path('subscribed.html', views.subscribed, name='subscribed'),
    path('toptags.html', views.toptags, name='toptags'),
    path('search_result.html', views.search_result, name='search_result'),
    url(r'^search_result/$', views.search_result, name='search_result'),
    path('toppodcasts.html', views.toppodcasts, name='toppodcasts'),
    path('episodes.html', views.episodes, name="episodes"),
    path('login_page.html', views.login, name="login"),
    url(r'^episodes/$', views.episodes, name='episodes'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)