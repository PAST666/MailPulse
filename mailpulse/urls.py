from django.contrib import admin
from django.urls import path
from users import urls as users_urls
from mailings import urls as mailings_urls
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from mailings.views import MainView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main'),
    path('users/', include(users_urls)),
    path('', include(mailings_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
