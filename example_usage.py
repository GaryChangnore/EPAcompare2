#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPA 專案比對工具使用範例
"""

from epa_project_comparator import EPAProjectComparator

# 範例 1：基本使用（自動判斷時間）
def example_basic():
    """基本使用範例"""
    excel_files = [
        'snapshot_2024_01.xlsx',
        'snapshot_2024_02.xlsx',
        'snapshot_2024_03.xlsx'
    ]
    
    comparator = EPAProjectComparator(excel_files)
    comparator.compare_and_export('output_basic.xlsx')


# 範例 2：手動指定日期
def example_with_dates():
    """手動指定日期範例"""
    excel_files = [
        'file1.xlsx',
        'file2.xlsx',
        'file3.xlsx'
    ]
    
    # 手動指定每個檔案對應的日期
    snapshot_dates = {
        'file1.xlsx': '2024/01/15',
        'file2.xlsx': '2024/02/20',
        'file3.xlsx': '2024/03/25'
    }
    
    comparator = EPAProjectComparator(excel_files, snapshot_dates)
    comparator.compare_and_export('output_with_dates.xlsx')


# 範例 3：處理多個檔案
def example_multiple_files():
    """處理多個檔案範例"""
    import glob
    
    # 自動尋找所有 Excel 檔案
    excel_files = sorted(glob.glob('epa_snapshots/*.xlsx'))
    
    if len(excel_files) < 2:
        print("❌ 錯誤：至少需要 2 個 Excel 檔案")
        return
    
    comparator = EPAProjectComparator(excel_files)
    comparator.compare_and_export('output_multiple.xlsx')


if __name__ == '__main__':
    print("EPA 專案比對工具 - 使用範例")
    print("=" * 50)
    print("\n請選擇要執行的範例：")
    print("1. 基本使用（自動判斷時間）")
    print("2. 手動指定日期")
    print("3. 處理多個檔案")
    
    choice = input("\n請輸入選項 (1-3): ").strip()
    
    if choice == '1':
        example_basic()
    elif choice == '2':
        example_with_dates()
    elif choice == '3':
        example_multiple_files()
    else:
        print("❌ 無效的選項")
