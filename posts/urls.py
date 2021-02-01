from django.urls import path
from .views import *
from .feeds import LatestPostsFeed

app_name = 'posts'

urlpatterns = [
    path('post/<int:pk>/<slug:slugy>/<int:year>/<int:month>/<int:day>/', PostDetailView.as_view(), name='post-detail'),
    path('categories/<slug:slug>/', PostCategories.as_view(), name='post-by-categories'),
    path('profile/<slug:username>/', ViewPostAuthorProfile.as_view(), name='view-author-profile'),
    path('<str:username>/posts/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/<slug:slug>/update/', PostUpdateView.as_view(), name='update-post'),
    path('post/<int:pk>/<slug:slug>/delete/', PostDeleteView.as_view(), name='delete-post'),
    path('tag/<slug:tag_slug>/', PostListView.as_view(), name='post_list_by_tag'),
    path('trending/', TrendingPostsView.as_view(), name='trending-posts'),
    path('feed/', LatestPostsFeed(), name='posts_feed'),
    path('create-post/', PostCreateView.as_view(), name='create-post'),
    path('categories/', PostCategories.as_view(), name='categories'),
    path('search', SearchView.as_view(), name='search'),
    path('', PostListView.as_view(), name='index'),
]
