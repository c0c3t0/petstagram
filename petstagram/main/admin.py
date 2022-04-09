from django.contrib import admin

from petstagram.main.models import Pet, PetPhoto


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')


@admin.register(PetPhoto)
class PetPhotoAdmin(admin.ModelAdmin):
    list_display = ('photo', 'likes')
