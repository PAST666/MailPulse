from django.contrib import admin
from django.urls import path
from mailings.views import MainView
from users import urls
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main'),
    path('users/', include(urls)),
]
