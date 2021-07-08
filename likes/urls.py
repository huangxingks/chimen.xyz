from django.urls import path

from . import views


app_name = 'likes'

urlpatterns = [
    path('like-update/', views.like_update, name='like_update')
]