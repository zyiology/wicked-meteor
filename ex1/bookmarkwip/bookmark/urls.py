from django.conf.urls import patterns, url
from bookmark import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'),
        url(r'^add_category/$', views.add_category, name='add_category'), # NEW MAPPING!
        url(r'^category/(?P<category_name_url>\w+)/add_page/$', views.add_page, name='add_page')
)