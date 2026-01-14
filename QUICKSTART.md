# EPA 專案比對工具 - 快速開始指南

## 安裝

```bash
pip install -r requirements.txt
```

## 快速使用

### 方法 1：命令列（最簡單）

```bash
python epa_project_comparator.py output.xlsx file1.xlsx file2.xlsx file3.xlsx
```

### 方法 2：Python 程式碼

```python
from epa_project_comparator import EPAProjectComparator

# 準備檔案
files = ['snapshot1.xlsx', 'snapshot2.xlsx', 'snapshot3.xlsx']

# 執行比對
comparator = EPAProjectComparator(files)
comparator.compare_and_export('result.xlsx')
```

## 輸出說明

### 🟡 黃色 = 有變動
- 最新時間點與前一個時間點相比，欄位值有差異
- 變動的儲存格 + Seq + Snapshot_Date + 專案名稱都會標黃

### 🔴 紅色 = 結構異常
- 不同檔案的欄位結構不一致
- 整列標示為紅色，提醒檢查資料來源

## 注意事項

1. **至少需要 2 個檔案**才能進行比對
2. **必須有 Project Name 或 Applicant Name 欄位**作為專案識別
3. **建議所有檔案欄位結構一致**，避免標示為紅色

## 常見問題

**Q: 如何手動指定日期？**
```bash
python epa_project_comparator.py output.xlsx \
  file1.xlsx --date file1.xlsx:2024/01/15 \
  file2.xlsx --date file2.xlsx:2024/02/20
```

**Q: 找不到專案比對欄位？**
- 確認 Excel 檔案包含 `Project Name` 或 `Applicant Name` 欄位
- 或修改程式碼中的 `PROJECT_KEY_COLUMNS` 設定

**Q: 所有專案都標紅色？**
- 檢查所有檔案的欄位名稱、順序、數量是否相同
- 欄位結構必須完全一致才能進行比對
