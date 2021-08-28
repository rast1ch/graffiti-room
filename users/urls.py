from django.urls import path
from .views import (
    ArtistCreateView,
    ArtistLoginView,
    ArtistChangeView,
    UserPostsListView,
    ArtistLogoutView,
    ArtistConfirmView,
    ArtistResetPassword,
    ArtistChangePassword,
    ArtistChangePasswordWithEmail
)

urlpatterns = [
    path('registration/', ArtistCreateView.as_view(), name="registration"),
    path('login/', ArtistLoginView.as_view(), name="login"),
    path('logout/', ArtistLogoutView.as_view(), name="logout"),
    path('reset_password', ArtistResetPassword.as_view(), name ="reset"),
    path('forgot_password',ArtistChangePasswordWithEmail.as_view(), name="forgot"),
    path('verify/<uuid:uuid>', ArtistConfirmView.as_view(), name="confirm"),
    path('change_password/<uuid:uuid>', ArtistChangePassword.as_view(), name="change_password"),
    path('<slug:slug>/change', ArtistChangeView.as_view(), name="change"),
    path('<slug:slug>/', UserPostsListView.as_view(), name="artist_posts"),
]
