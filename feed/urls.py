from django.urls import path
from . import views
    
urlpatterns = [
    path('feed/',views.PostListView.as_view(), name='feed'),
    path('post/create', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/update', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete', views.PostDeleteView.as_view(), name='post_delete'),
    path('',views.FeedRedirectView.as_view())
    
]
