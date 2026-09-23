from django.contrib import admin
from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'company',
        'position',
        'user',
        'status',
        'priority',
        'employment_type',
        'date_applied',
        'salary',
        'updated_at',
    )
    list_filter = (
        'status',
        'priority',
        'employment_type',
        'created_at',
    )
    search_fields = (
        'company',
        'position',
        'location',
        'user__username',
        'user__email',
    )
    ordering = ('-updated_at',)
    date_hierarchy = 'created_at'
