# EPA 專案版本比對工具

一個用於比對多個時間點 EPA 專案 Excel 檔案的資料工程工具，自動標示實質變動，協助分析師快速審閱。

## 功能特色

- 📊 **自動比對**：比較多個時間點的 EPA 專案資料
- 🎨 **顏色標記**：🟡 黃色標示變動，🔴 紅色標示結構異常
- 🌐 **網頁介面**：Streamlit 提供友善的上傳和下載介面
- 🔍 **智能比對**：只比較最新與前一個時間點，避免誤報
- ✅ **結構檢查**：自動檢查欄位結構一致性

## 快速開始

### 安裝

```bash
pip install -r requirements.txt
```

### 使用網頁介面（推薦）

```bash
# 啟動 Streamlit 應用
./run_app.sh
# 或
streamlit run app.py
```

瀏覽器會自動開啟 http://localhost:8501

### 使用命令列

```bash
python epa_project_comparator.py output.xlsx file1.xlsx file2.xlsx file3.xlsx
```

## 檔案說明

- `epa_project_comparator.py` - 核心比對工具（命令列版本）
- `app.py` - Streamlit 網頁介面
- `example_usage.py` - Python 使用範例
- `run_app.sh` - 快速啟動腳本

## 文件

- [完整工具說明](README_EPA_COMPARATOR.md) - 詳細功能和使用說明
- [網頁介面說明](README_STREAMLIT.md) - Streamlit 介面使用指南
- [快速開始指南](QUICKSTART.md) - 快速上手指南
- [Git 設定說明](GIT_SETUP.md) - Git 倉庫設定指南

## 輸出說明

### 🟡 黃色標示
最新時間點與前一個時間點相比，欄位值有差異的儲存格。

### 🔴 紅色標示
不同檔案的欄位結構不一致（欄位名稱、順序、數量不同）。

## 系統需求

- Python 3.8+
- pandas >= 2.0.0
- openpyxl >= 3.1.0
- streamlit >= 1.28.0

## 授權

本工具專為能源/法規分析師設計，用於 EPA 專案資料分析。

## 貢獻

歡迎提出問題和改進建議。
