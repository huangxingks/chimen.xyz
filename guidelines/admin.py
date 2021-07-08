from django.contrib import admin

from .models import Subject, University, Guideline


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Guideline)
class GuidelineAdmin(admin.ModelAdmin):
    list_dispaly = ('id', 'subject', 'university', 'school')
    ordering = ("subject",)