from django.urls import path

from . import views


app_name = 'chimen_notifications'

urlpatterns = [
    path('', views.chimen_notifications, name='chimen_notifications'),
    path('<int:chimen_notification_pk>/', views.chimen_notification, name='chimen_notification'),
    path('delete_notifications_read/', views.delete_notifications_read, name='delete_notifications_read')
]