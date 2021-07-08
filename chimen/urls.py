from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('user/', include('user.urls')),      
    path('guidelines/', include('guidelines.urls')),
    path('comments/', include('comments.urls')),
    path('likes/', include('likes.urls')),
    path('applications/', include('applications.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)