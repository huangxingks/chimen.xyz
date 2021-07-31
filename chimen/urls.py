from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('', views.home, name='home'),
    path('search/', views.search, name="search"),

    path('user/', include('user.urls')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    path('chimen_notifications/', include('chimen_notifications.urls')),

    path('guidelines/', include('guidelines.urls')),
    path('applications/', include('applications.urls')),

    path('comments/', include('comments.urls')),
    path('likes/', include('likes.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)