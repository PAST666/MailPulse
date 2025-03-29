from django.contrib import admin
from django.urls import include, path

from .views import MainView

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
]
