from django.contrib import admin
from .models import Schedule

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('subject', 'date', 'grade', 'study_type', 'type')
    list_filter = ('grade', 'study_type', 'type', 'date')
    search_fields = ('subject__name', 'description')
    date_hierarchy = 'date'