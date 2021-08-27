from django.urls import path
from .views import (
    ArtistCreateView,
    ArtistLoginView,
    ArtistChangeView,
    UserPostsListView,
    ArtistLogoutView,
    ArtistConfirmView
)

urlpatterns = [
    path('registration/', ArtistCreateView.as_view(), name="registration"),
    path('login/', ArtistLoginView.as_view(), name="login"),
    path('logout/', ArtistLogoutView.as_view(), name="logout"),
    path('verify/<uuid:uuid>', ArtistConfirmView.as_view(), name="confirm"),
    path('<slug:slug>/change', ArtistChangeView.as_view(), name="change"),
    path('<slug:slug>/', UserPostsListView.as_view(), name="artist_posts"),
]
