# Git 設定指南

## 應該加入 Git 的檔案

### 核心程式檔案
- ✅ `epa_project_comparator.py` - 核心比對工具
- ✅ `app.py` - Streamlit 網頁介面
- ✅ `example_usage.py` - 使用範例

### 設定和依賴
- ✅ `requirements.txt` - Python 依賴套件
- ✅ `run_app.sh` - 啟動腳本

### 說明文件
- ✅ `README_EPA_COMPARATOR.md` - 工具完整說明
- ✅ `README_STREAMLIT.md` - 網頁介面說明
- ✅ `QUICKSTART.md` - 快速開始指南
- ✅ `啟動說明.txt` - 快速參考
- ✅ `GIT_SETUP.md` - 本檔案

### 設定檔案
- ✅ `.gitignore` - Git 忽略規則

## 不應該加入 Git 的檔案

以下檔案已自動被 `.gitignore` 忽略：

- ❌ `__pycache__/` - Python 快取檔案
- ❌ `*.xlsx`, `*.xls` - Excel 測試檔案
- ❌ `.streamlit/config.toml` - 個人 Streamlit 設定
- ❌ `untitled*.py` - 臨時測試檔案
- ❌ `output_*.xlsx` - 比對結果檔案
- ❌ `.DS_Store` - macOS 系統檔案

## Git 初始化步驟

### 1. 初始化 Git 倉庫

```bash
cd /Users/gary
git init
```

### 2. 加入檔案

```bash
# 加入所有應該追蹤的檔案
git add epa_project_comparator.py
git add app.py
git add example_usage.py
git add requirements.txt
git add run_app.sh
git add README_EPA_COMPARATOR.md
git add README_STREAMLIT.md
git add QUICKSTART.md
git add 啟動說明.txt
git add GIT_SETUP.md
git add .gitignore

# 或一次加入所有（會自動遵守 .gitignore）
git add .
```

### 3. 檢查要提交的檔案

```bash
git status
```

確認只包含應該加入的檔案。

### 4. 提交

```bash
git commit -m "Initial commit: EPA 專案版本比對工具

- 核心比對工具 (epa_project_comparator.py)
- Streamlit 網頁介面 (app.py)
- 完整說明文件
- 啟動腳本和使用範例"
```

### 5. 連接到遠端倉庫（可選）

```bash
# 在 GitHub/GitLab 建立倉庫後
git remote add origin <你的倉庫URL>
git branch -M main
git push -u origin main
```

## 快速檢查清單

在提交前，確認：

- [ ] 已建立 `.gitignore`
- [ ] 沒有包含個人敏感資訊
- [ ] 沒有包含測試用的 Excel 檔案
- [ ] 沒有包含 `__pycache__` 目錄
- [ ] README 檔案完整
- [ ] 程式碼沒有硬編碼的路徑或密碼

## 檔案結構建議

```
epa-project-comparator/
├── epa_project_comparator.py    # 核心工具
├── app.py                       # Streamlit 介面
├── example_usage.py             # 使用範例
├── requirements.txt             # 依賴套件
├── run_app.sh                   # 啟動腳本
├── README_EPA_COMPARATOR.md     # 工具說明
├── README_STREAMLIT.md          # 介面說明
├── QUICKSTART.md                # 快速指南
├── 啟動說明.txt                  # 快速參考
├── GIT_SETUP.md                 # Git 設定說明
└── .gitignore                   # Git 忽略規則
```

## 後續維護

### 更新檔案後

```bash
git add <修改的檔案>
git commit -m "描述修改內容"
git push
```

### 查看變更

```bash
git status          # 查看狀態
git diff            # 查看變更內容
git log             # 查看提交歷史
```
