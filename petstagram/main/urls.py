from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from petstagram.main.views.generic import HomeView, DashboardView
from petstagram.main.views.pet_photos import like_pet_photo, \
    ShowPhotoDetailsView, EditPhotoView, CreatePhotoView, DeletePhotoView
from petstagram.main.views.pets import CreatePetView, EditPetView, DeletePetView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('pet/add/', CreatePetView.as_view(), name='add pet'),
    path('pet/edit/<int:pk>/', EditPetView.as_view(), name='edit pet'),
    path('pet/delete/<int:pk>/', DeletePetView.as_view(), name='delete pet'),


    path('photo/add/', CreatePhotoView.as_view(), name='add photo'),
    path('photo/edit/<int:pk>/', EditPhotoView.as_view(), name='edit photo'),
    path('photo/details/<int:pk>/', ShowPhotoDetailsView.as_view(), name='show photo details'),
    path('photo/like/<int:pk>', like_pet_photo, name='like pet photo'),
    path('photo/delete/<int:pk>/', DeletePhotoView.as_view(), name='delete photo')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)