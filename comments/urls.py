from django.urls import path

from . import views


app_name = 'comments'

urlpatterns = [
    path('comment-update/', views.comment_update, name='comment_update')
]