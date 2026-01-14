# EPA 專案版本比對工具

## 功能說明

此工具用於比對多個不同時間點的 EPA 專案 Excel 檔案，自動標示實質變動，協助分析師快速審閱。

## 主要特性

- ✅ 自動判斷檔案時間（支援手動指定）
- ✅ 欄位結構檢查（防呆機制）
- ✅ 專案自動合併（基於專案名稱）
- ✅ 顏色標記變動（🟡 黃色 = 變動，🔴 紅色 = 結構異常）
- ✅ 只比較最新與前一個時間點（避免誤報）

## 安裝需求

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
python epa_project_comparator.py <輸出檔案> <檔案1> <檔案2> [檔案3] ...
```

**範例：**
```bash
python epa_project_comparator.py result.xlsx snapshot_2024_01.xlsx snapshot_2024_02.xlsx snapshot_2024_03.xlsx
```

### 手動指定日期

如果檔案時間無法從檔案系統取得，可手動指定：

```bash
python epa_project_comparator.py result.xlsx \
  file1.xlsx --date file1.xlsx:2024/01/15 \
  file2.xlsx --date file2.xlsx:2024/02/20 \
  file3.xlsx --date file3.xlsx:2024/03/25
```

### Python 程式碼使用

```python
from epa_project_comparator import EPAProjectComparator

# 準備檔案列表
excel_files = [
    'snapshot_2024_01.xlsx',
    'snapshot_2024_02.xlsx',
    'snapshot_2024_03.xlsx'
]

# 可選：手動指定日期
snapshot_dates = {
    'snapshot_2024_01.xlsx': '2024/01/15',
    'snapshot_2024_02.xlsx': '2024/02/20',
    'snapshot_2024_03.xlsx': '2024/03/25'
}

# 執行比對
comparator = EPAProjectComparator(excel_files, snapshot_dates)
comparator.compare_and_export('output.xlsx')
```

## 輸出說明

### 新增欄位

輸出檔案會在最前方新增兩個欄位：

1. **Seq**：整數序列（1, 2, 3...），數字越大代表資料越新
2. **Snapshot_Date**：該檔案代表的資料時間（YYYY/MM/DD 格式）

### 顏色標記規則

#### 🟡 黃色標示（實質資料變動）

當「最新時間點」的專案與「前一個時間點」相比，有任何欄位值不同時：

- 該「不同的儲存格」標示為 🟡 黃色
- 同一列的 **Seq**、**Snapshot_Date**、**專案名稱欄位** 也一併標示為 🟡 黃色

**目的：** 讓使用者一眼就知道「這一筆有變動」

#### 🔴 紅色標示（結構性異常）

當不同檔案的欄位結構不一致時（欄位數量、名稱、順序不同）：

- 不進行欄位比對
- 將最新時間點的整列標示為 🔴 紅色

**目的：** 提醒使用者資料來源結構異常或上傳錯誤

### 不進行比對的欄位

以下欄位即使不同也不會標色：

- `Seq`
- `Snapshot_Date`
- `Comments`、`Notes`、`備註`、`註記` 等純描述性備註欄位

## 專案比對邏輯

### 比對 Key

工具會依以下優先順序尋找專案比對欄位：

1. `Project Name`
2. `Applicant Name`
3. `專案名稱`
4. `申請人名稱`

### 比對規則

- 去除前後空白
- 忽略大小寫
- 其餘內容必須完全一致

### 排序規則

同一專案在不同時間點的資料會：

- 上下疊在一起
- 依 `Snapshot_Date` 由舊 → 新排序

## 注意事項

1. **檔案格式**：支援 `.xlsx` 和 `.xls` 格式
2. **專案識別**：必須有 `Project Name` 或 `Applicant Name` 欄位
3. **欄位一致性**：建議所有檔案的欄位結構保持一致
4. **時間判斷**：若未手動指定，會使用檔案的修改時間

## 設計原則

此工具專為能源/法規分析師設計，重點是：

- ✅ 快速掃描變動
- ✅ 避免誤報（false positive）
- ✅ 寧可少標，也不要全表變黃

## 疑難排解

### 錯誤：找不到專案比對欄位

**原因：** Excel 檔案中沒有 `Project Name` 或 `Applicant Name` 欄位

**解決：** 確認檔案包含上述欄位之一，或修改程式碼中的 `PROJECT_KEY_COLUMNS` 設定

### 所有專案都標示為紅色

**原因：** 不同檔案的欄位結構不一致

**解決：** 檢查所有檔案的欄位名稱、順序、數量是否相同

### 日期格式錯誤

**原因：** 手動指定的日期格式不正確

**解決：** 使用 `YYYY/MM/DD` 格式，例如：`2024/01/15`
