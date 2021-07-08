from django.urls import path

from . import views


app_name = 'user'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('modal-login/', views.modal_login, name='modal_login'),
    path('logout/', views.logout, name='logout'),
    path('user-info/', views.user_info, name='user_info'),
    path('change-displayname/', views.change_displayname, name='change_displayname'),
    path('change-email/', views.change_email, name='change_email'),
    path('change-password/', views.change_password, name='change_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('send-verification-code/', views.send_verification_code, name='send_verification_code'),
]