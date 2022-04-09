from django.urls import path

from petstagram.accounts.views import UserRegisterView, UserLoginView, EditProfileView, \
    ChangeUserPasswordView, ProfileDetailsView, DeleteProfileView

urlpatterns = (
    path('create-profile/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('edit-profile/<int:pk>/', EditProfileView.as_view(), name='edit profile'),
    path('delete-profile/<int:pk>/', DeleteProfileView.as_view(), name='delete profile'),
    # path('edit-password/<int:pk>/', ChangeUserPasswordView.as_view(), name='edit password'),

)