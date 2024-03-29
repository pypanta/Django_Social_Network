from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('api/', include('accounts.api.urls')),
    path('api/posts/', include('posts.api.urls')),
    path('api/chat/', include('chat.api.urls')),
    path('api/notifications/', include('notifications.api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
