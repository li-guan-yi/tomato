# 番茄鐘待辦清單 (Tomato Todo List)

一個結合工作待辦清單和番茄鐘時間管理法的 Django 應用程式。

## 功能特色

### 工作待辦清單
- ✅ 支援增刪改查 (CRUD) 功能
- 📅 可設定開始日期和結束日期
- ⚠️ 結束日期到期時會有變色提醒
- 🔍 支援搜尋和篩選功能
- 📊 狀態管理（未完成、已完成、過期、今天到期）

### 番茄鐘模組
- ⏰ 標準番茄鐘：工作 25 分鐘、休息 5 分鐘
- 🎯 可開始或暫停倒數計時
- 🔄 自動循環：工作 → 休息 → 工作
- ⚙️ 可客製化時間長度
- 📈 進度條顯示
- 📝 完成後顯示該時段任務所達時間長度
- 📊 歷史記錄和統計分析

## 技術架構

- **後端框架**: Django 5.2.5
- **資料庫**: SQLite
- **前端框架**: Bootstrap 5.3.0
- **JavaScript 庫**: jQuery 3.7.0
- **表單處理**: Django Crispy Forms + Bootstrap 5
- **圖示**: Bootstrap Icons

## 安裝與執行

### 1. 環境需求
- Python 3.8+
- pip

### 2. 安裝步驟

```bash
# 克隆專案
git clone <repository-url>
cd tomato

# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt

# 執行資料庫遷移
python manage.py makemigrations
python manage.py migrate

# 建立超級使用者（可選）
python manage.py createsuperuser

# 啟動開發伺服器
python manage.py runserver
```

### 3. 訪問應用程式

- 主頁面: http://127.0.0.1:8000/
- 管理員介面: http://127.0.0.1:8000/admin/
  - 預設帳號: admin
  - 預設密碼: 請在建立超級使用者時設定

## 使用說明

### 待辦事項管理

1. **新增待辦事項**
   - 點擊「新增」按鈕
   - 填寫標題、描述、開始日期、結束日期
   - 系統會自動設定合理的預設日期

2. **管理待辦事項**
   - 在列表中查看所有待辦事項
   - 使用篩選器按狀態或搜尋關鍵字
   - 點擊勾選框標記完成
   - 使用編輯和刪除按鈕管理項目

3. **日期提醒**
   - 過期項目會以紅色背景顯示
   - 今天到期的項目會以黃色背景顯示
   - 已完成的項目會以綠色背景顯示並加上刪除線

### 番茄鐘使用

1. **基本操作**
   - 在首頁選擇要工作的待辦事項
   - 點擊「開始」按鈕開始計時
   - 可隨時暫停或停止計時
   - 時段結束時會自動提醒

2. **時間設定**
   - 前往「設定」頁面自訂時間長度
   - 可調整工作時長、休息時長、長休息時長
   - 可設定長休息前的工作時段數

3. **歷史記錄**
   - 查看所有完成的番茄鐘時段
   - 統計工作時間和效率
   - 按時段類型、待辦事項、日期篩選

## 專案結構

```
tomato/
├── manage.py
├── requirements.txt
├── README.md
├── tomato_project/          # Django 專案設定
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── todo/                    # 主要應用程式
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/               # HTML 模板
│   ├── base.html
│   └── todo/
│       ├── home.html
│       ├── todo_list.html
│       ├── todo_form.html
│       ├── todo_confirm_delete.html
│       ├── pomodoro_settings.html
│       └── pomodoro_history.html
└── static/                  # 靜態檔案
```

## 資料模型

### Todo (待辦事項)
- `title`: 標題
- `description`: 描述
- `start_date`: 開始日期
- `end_date`: 結束日期
- `completed`: 完成狀態
- `created_at`: 建立時間
- `updated_at`: 更新時間

### PomodoroSession (番茄鐘時段)
- `todo`: 關聯的待辦事項
- `session_type`: 時段類型 (工作/休息)
- `duration`: 預定時長
- `actual_duration`: 實際時長
- `started_at`: 開始時間
- `completed_at`: 完成時間
- `is_completed`: 完成狀態

### PomodoroSettings (番茄鐘設定)
- `work_duration`: 工作時長
- `break_duration`: 休息時長
- `long_break_duration`: 長休息時長
- `sessions_before_long_break`: 長休息前工作時段數

## 開發說明

### 新增功能
1. 在 `models.py` 中定義資料模型
2. 執行 `python manage.py makemigrations` 建立遷移檔案
3. 執行 `python manage.py migrate` 套用遷移
4. 在 `views.py` 中實作視圖邏輯
5. 在 `urls.py` 中設定 URL 路由
6. 建立對應的 HTML 模板

### 自訂樣式
- 主要樣式定義在 `templates/base.html` 的 `<style>` 區塊
- 使用 Bootstrap 5 的 CSS 類別
- 可新增自訂 CSS 檔案到 `static/` 目錄

## 授權

本專案採用 MIT 授權條款。

## 貢獻

歡迎提交 Issue 和 Pull Request 來改善這個專案！
