from django.urls import path
from .views import SignupView, LoginView, UploadImageView, UploadClothingImageView, avatar_list, UserProfileView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('uploadimage/', UploadImageView.as_view(), name='uploadimage'),
    path('uploadclothing/', UploadClothingImageView.as_view(), name='uploadclothing'),
    path('avatars/', avatar_list, name='avatar_list'),
    path('user-profile/', UserProfileView.as_view(), name='user-profile')



]

