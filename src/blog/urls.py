from django.urls import path
from . import views

from .feeds import LatestPostsFeed


app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,name='post_detail'),
    path('tag/<slug:tag_slug>/',views.post_list, name='post_list_by_tag'),
    path('<int:id>/', views.post_edit, name='post_edit'),
    #re_path(r'^(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    # re_path(r'^search/$', views.post_search, name='post_search'),
    path('<slug:slug>/', views.category_list, name='category_list')
]


