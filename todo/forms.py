from django import forms
from .models import Todo, PomodoroSettings

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '輸入待辦事項標題'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '輸入描述（可選）'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'title': '標題',
            'description': '描述',
            'start_date': '開始日期',
            'end_date': '結束日期',
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError('開始日期不能晚於結束日期')
        
        return cleaned_data

class PomodoroSettingsForm(forms.ModelForm):
    class Meta:
        model = PomodoroSettings
        fields = ['work_duration', 'break_duration', 'long_break_duration', 'sessions_before_long_break']
        widgets = {
            'work_duration': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 60}),
            'break_duration': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 30}),
            'long_break_duration': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 60}),
            'sessions_before_long_break': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
        }
        labels = {
            'work_duration': '工作時長（分鐘）',
            'break_duration': '休息時長（分鐘）',
            'long_break_duration': '長休息時長（分鐘）',
            'sessions_before_long_break': '長休息前工作時段數',
        }
