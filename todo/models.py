from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

class Todo(models.Model):
    title = models.CharField(max_length=200, verbose_name='標題')
    description = models.TextField(blank=True, verbose_name='描述')
    start_date = models.DateField(verbose_name='開始日期')
    end_date = models.DateField(verbose_name='結束日期')
    completed = models.BooleanField(default=False, verbose_name='已完成')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')

    class Meta:
        verbose_name = '待辦事項'
        verbose_name_plural = '待辦事項'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        """檢查是否已過期"""
        return self.end_date < timezone.now().date() and not self.completed

    @property
    def is_due_today(self):
        """檢查是否今天到期"""
        return self.end_date == timezone.now().date() and not self.completed

class PomodoroSession(models.Model):
    SESSION_TYPES = [
        ('work', '工作'),
        ('break', '休息'),
    ]
    
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='pomodoro_sessions', verbose_name='待辦事項')
    session_type = models.CharField(max_length=5, choices=SESSION_TYPES, verbose_name='時段類型')
    duration = models.IntegerField(verbose_name='時長(分鐘)')
    actual_duration = models.FloatField(default=0.0, verbose_name='實際時長(分鐘)')
    started_at = models.DateTimeField(verbose_name='開始時間')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成時間')
    is_completed = models.BooleanField(default=False, verbose_name='已完成')
    
    class Meta:
        verbose_name = '番茄鐘時段'
        verbose_name_plural = '番茄鐘時段'
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.todo.title} - {self.get_session_type_display()}"

    def complete_session(self):
        """完成時段"""
        if not self.is_completed:
            self.completed_at = timezone.now()
            self.is_completed = True
            if self.completed_at and self.started_at:
                duration = self.completed_at - self.started_at
                # 計算實際時長（秒），然後轉換為分鐘，保留小數點後2位
                total_seconds = duration.total_seconds()
                self.actual_duration = max(0.01, round(total_seconds / 60, 2))
            self.save()

class PomodoroSettings(models.Model):
    work_duration = models.IntegerField(default=25, verbose_name='工作時長(分鐘)')
    break_duration = models.IntegerField(default=5, verbose_name='休息時長(分鐘)')
    long_break_duration = models.IntegerField(default=15, verbose_name='長休息時長(分鐘)')
    sessions_before_long_break = models.IntegerField(default=4, verbose_name='長休息前工作時段數')
    
    class Meta:
        verbose_name = '番茄鐘設定'
        verbose_name_plural = '番茄鐘設定'

    def __str__(self):
        return f"工作{self.work_duration}分鐘，休息{self.break_duration}分鐘"
