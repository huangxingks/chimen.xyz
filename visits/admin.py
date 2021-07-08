from django.contrib import admin

from .models import VisitNum


@admin.register(VisitNum)
class VisitNumAdmin(admin.ModelAdmin):
    list_dispaly = ('content_object', 'number')