from django.urls import path
from .views import (
    ArtistCreateView,
    ArtistChangeView,
    UserPostsListView,
)
urlpatterns = [
    path('registration/', ArtistCreateView.as_view()),
    path('<slug:slug>/change', ArtistChangeView.as_view()),
    path('<slug:slug>/',UserPostsListView.as_view(),name="artist_detail")
]
