from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('petstagram.main.urls')),
    path('accounts/', include('petstagram.accounts.urls')),
]
