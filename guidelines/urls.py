from django.urls import path

from . import views


app_name = 'guidelines'

urlpatterns = [
    path('guideline-list/', views.guideline_list, name='guideline_list'),
    #path('guideline-ongoing/', views.guideline_ongoing, name='guideline_ongoing'),
    #path('guideline-coming/', views.guideline_coming, name='guideline_coming'),
    path('guideline-by-subject/<int:subject_pk>/', views.guideline_by_subject, name='guideline_by_subject'),
    path('guideline-detail/<int:guideline_pk>/', views.guideline_detail, name='guideline_detail'),
]
