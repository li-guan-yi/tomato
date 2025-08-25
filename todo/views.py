from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q
from .models import Todo, PomodoroSession, PomodoroSettings
from .forms import TodoForm, PomodoroSettingsForm
import json

def home(request):
    """首頁 - 顯示待辦事項列表和番茄鐘"""
    todos = Todo.objects.all()
    settings = PomodoroSettings.objects.first()
    if not settings:
        settings = PomodoroSettings.objects.create()
    
    # 獲取今天的待辦事項
    today = timezone.now().date()
    today_todos = todos.filter(end_date=today, completed=False)
    overdue_todos = todos.filter(end_date__lt=today, completed=False)
    
    context = {
        'todos': todos,
        'today_todos': today_todos,
        'overdue_todos': overdue_todos,
        'settings': settings,
    }
    return render(request, 'todo/home.html', context)

def todo_list(request):
    """待辦事項列表"""
    todos = Todo.objects.all()
    return render(request, 'todo/todo_list.html', {'todos': todos})

def todo_create(request):
    """創建待辦事項"""
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '待辦事項創建成功！')
            return redirect('todo_list')
    else:
        form = TodoForm()
    
    return render(request, 'todo/todo_form.html', {'form': form, 'title': '新增待辦事項'})

def todo_update(request, pk):
    """更新待辦事項"""
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, '待辦事項更新成功！')
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    
    return render(request, 'todo/todo_form.html', {'form': form, 'title': '編輯待辦事項'})

def todo_delete(request, pk):
    """刪除待辦事項"""
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.delete()
        messages.success(request, '待辦事項刪除成功！')
        return redirect('todo_list')
    
    return render(request, 'todo/todo_confirm_delete.html', {'todo': todo})

def todo_toggle(request, pk):
    """切換待辦事項完成狀態"""
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'completed': todo.completed})
    
    messages.success(request, f'待辦事項已{"完成" if todo.completed else "標記為未完成"}！')
    return redirect('todo_list')

def pomodoro_settings(request):
    """番茄鐘設定"""
    settings = PomodoroSettings.objects.first()
    if not settings:
        settings = PomodoroSettings.objects.create()
    
    if request.method == 'POST':
        form = PomodoroSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, '番茄鐘設定已更新！')
            return redirect('home')
    else:
        form = PomodoroSettingsForm(instance=settings)
    
    return render(request, 'todo/pomodoro_settings.html', {'form': form})

@csrf_exempt
def pomodoro_start(request):
    """開始番茄鐘時段"""
    if request.method == 'POST':
        data = json.loads(request.body)
        todo_id = data.get('todo_id')
        session_type = data.get('session_type', 'work')
        
        todo = get_object_or_404(Todo, pk=todo_id)
        settings = PomodoroSettings.objects.first()
        if not settings:
            settings = PomodoroSettings.objects.create()
        
        # 設定時長
        if session_type == 'work':
            duration = settings.work_duration
        else:
            duration = settings.break_duration
        
        # 創建新的番茄鐘時段
        session = PomodoroSession.objects.create(
            todo=todo,
            session_type=session_type,
            duration=duration,
            started_at=timezone.now()
        )
        
        return JsonResponse({
            'session_id': session.id,
            'duration': duration,
            'session_type': session_type
        })
    
    return JsonResponse({'error': '無效的請求'}, status=400)

@csrf_exempt
def pomodoro_complete(request):
    """完成番茄鐘時段"""
    if request.method == 'POST':
        data = json.loads(request.body)
        session_id = data.get('session_id')
        
        session = get_object_or_404(PomodoroSession, pk=session_id)
        session.complete_session()
        
        return JsonResponse({
            'actual_duration': session.actual_duration,
            'session_type': session.session_type
        })
    
    return JsonResponse({'error': '無效的請求'}, status=400)

def pomodoro_history(request):
    """番茄鐘歷史記錄"""
    sessions = PomodoroSession.objects.filter(is_completed=True).order_by('-completed_at')
    
    # 計算統計資料
    work_sessions = sessions.filter(session_type='work')
    break_sessions = sessions.filter(session_type='break')
    
    total_work_minutes = sum(session.actual_duration for session in work_sessions)
    total_hours = total_work_minutes // 60
    total_minutes = total_work_minutes % 60
    
    context = {
        'sessions': sessions,
        'work_sessions_count': work_sessions.count(),
        'break_sessions_count': break_sessions.count(),
        'total_hours': total_hours,
        'total_minutes': total_minutes,
        'todos': Todo.objects.all(),
    }
    return render(request, 'todo/pomodoro_history.html', context)
