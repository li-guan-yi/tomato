from django.contrib import admin
from .models import Todo, PomodoroSession, PomodoroSettings

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'completed', 'created_at']
    list_filter = ['completed', 'start_date', 'end_date', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['completed']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('基本資訊', {
            'fields': ('title', 'description')
        }),
        ('日期設定', {
            'fields': ('start_date', 'end_date')
        }),
        ('狀態', {
            'fields': ('completed',)
        }),
    )

@admin.register(PomodoroSession)
class PomodoroSessionAdmin(admin.ModelAdmin):
    list_display = ['todo', 'session_type', 'duration', 'actual_duration', 'started_at', 'completed_at', 'is_completed']
    list_filter = ['session_type', 'is_completed', 'started_at', 'completed_at']
    search_fields = ['todo__title']
    date_hierarchy = 'started_at'
    
    fieldsets = (
        ('基本資訊', {
            'fields': ('todo', 'session_type', 'duration')
        }),
        ('時間記錄', {
            'fields': ('started_at', 'completed_at', 'actual_duration')
        }),
        ('狀態', {
            'fields': ('is_completed',)
        }),
    )
    
    readonly_fields = ['actual_duration']

@admin.register(PomodoroSettings)
class PomodoroSettingsAdmin(admin.ModelAdmin):
    list_display = ['work_duration', 'break_duration', 'long_break_duration', 'sessions_before_long_break']
    
    def has_add_permission(self, request):
        # 只允許一個設定實例
        return not PomodoroSettings.objects.exists()
