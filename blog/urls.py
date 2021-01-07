from . import views
from django.urls import path,include
from .feeds import LatestPostsFeed

app_name = "blog"

urlpatterns = [
    path('', views.PostIndex, name='index'),
    path('tag/<str:tag_slug>',views.PostIndex,name='index_tag'),
    path('category/<str:cat_slug>',views.PostIndex,name='index_category'),
    path('<str:slug>/', views.PostDetail, name='single'),
    path("feed/rss", LatestPostsFeed(), name="feed"),
]
