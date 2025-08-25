#!/usr/bin/env python
"""
簡單的應用程式測試腳本
"""
import os
import sys
import django
from datetime import date, timedelta

# 設定 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tomato_project.settings')
django.setup()

from todo.models import Todo, PomodoroSettings

def test_basic_functionality():
    """測試基本功能"""
    print("🧪 開始測試基本功能...")
    
    # 測試創建番茄鐘設定
    try:
        settings = PomodoroSettings.objects.first()
        if not settings:
            settings = PomodoroSettings.objects.create()
        print("✅ 番茄鐘設定創建成功")
    except Exception as e:
        print(f"❌ 番茄鐘設定創建失敗: {e}")
        return False
    
    # 測試創建待辦事項
    try:
        today = date.today()
        todo = Todo.objects.create(
            title="測試待辦事項",
            description="這是一個測試用的待辦事項",
            start_date=today,
            end_date=today + timedelta(days=7)
        )
        print("✅ 待辦事項創建成功")
    except Exception as e:
        print(f"❌ 待辦事項創建失敗: {e}")
        return False
    
    # 測試查詢功能
    try:
        todos = Todo.objects.all()
        print(f"✅ 查詢到 {todos.count()} 個待辦事項")
    except Exception as e:
        print(f"❌ 查詢失敗: {e}")
        return False
    
    # 測試更新功能
    try:
        todo.completed = True
        todo.save()
        print("✅ 待辦事項更新成功")
    except Exception as e:
        print(f"❌ 更新失敗: {e}")
        return False
    
    # 測試刪除功能
    try:
        todo.delete()
        print("✅ 待辦事項刪除成功")
    except Exception as e:
        print(f"❌ 刪除失敗: {e}")
        return False
    
    print("🎉 所有基本功能測試通過！")
    return True

def test_model_properties():
    """測試模型屬性"""
    print("\n🧪 開始測試模型屬性...")
    
    try:
        # 創建測試待辦事項
        today = date.today()
        overdue_todo = Todo.objects.create(
            title="過期待辦事項",
            start_date=today - timedelta(days=10),
            end_date=today - timedelta(days=1)
        )
        
        today_todo = Todo.objects.create(
            title="今天到期待辦事項",
            start_date=today - timedelta(days=5),
            end_date=today
        )
        
        # 測試過期屬性
        assert overdue_todo.is_overdue == True, "過期檢查失敗"
        print("✅ 過期檢查功能正常")
        
        # 測試今天到期屬性
        assert today_todo.is_due_today == True, "今天到期檢查失敗"
        print("✅ 今天到期檢查功能正常")
        
        # 清理測試資料
        overdue_todo.delete()
        today_todo.delete()
        
        print("🎉 模型屬性測試通過！")
        return True
        
    except Exception as e:
        print(f"❌ 模型屬性測試失敗: {e}")
        return False

if __name__ == "__main__":
    print("🚀 開始測試番茄鐘待辦清單應用程式...")
    print("=" * 50)
    
    success = True
    success &= test_basic_functionality()
    success &= test_model_properties()
    
    print("=" * 50)
    if success:
        print("🎉 所有測試通過！應用程式運行正常。")
        print("\n📝 下一步：")
        print("1. 執行 'python manage.py runserver' 啟動開發伺服器")
        print("2. 訪問 http://127.0.0.1:8000/ 查看應用程式")
        print("3. 訪問 http://127.0.0.1:8000/admin/ 進入管理介面")
    else:
        print("❌ 部分測試失敗，請檢查錯誤訊息。")
    
    sys.exit(0 if success else 1)
