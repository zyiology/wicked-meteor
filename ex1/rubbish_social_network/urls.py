from django.conf.urls import patterns, include, url
import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ex1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^detail/', views.user_detail, name='user_detail'),
    url(r'^users/', views.user_list, name='user_list'),
    url(r'^(?P<username>\w+)/followers/', views.user_followers, name='user_followers'),
    url(r'^(?P<username>\w+)/following/', views.user_following, name='user_following')
)