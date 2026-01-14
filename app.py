#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPA 專案版本比對工具 - Streamlit 網頁介面
"""

import streamlit as st
import pandas as pd
import os
import tempfile
from pathlib import Path
from datetime import datetime
from epa_project_comparator import EPAProjectComparator
import io

# 設定頁面
st.set_page_config(
    page_title="EPA 專案版本比對工具",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 標題
st.title("📊 EPA 專案版本比對工具")
st.markdown("---")

# 側邊欄：使用說明
with st.sidebar:
    st.header("📖 使用步驟")
    
    with st.expander("🔍 詳細步驟說明", expanded=True):
        st.markdown("""
        **步驟 1：上傳 Excel 檔案**
        - 點擊主畫面的「選擇檔案」按鈕
        - 選擇 **2 個或以上** 的 Excel 檔案
        - 支援 `.xlsx` 和 `.xls` 格式
        - 這些檔案代表不同時間點的 EPA 專案資料快照
        
        **步驟 2：確認檔案列表**
        - 檢查上傳的檔案名稱和大小
        - 確認檔案數量足夠（至少 2 個）
        - 系統會依檔案修改時間自動排序
        
        **步驟 3：執行比對**
        - 點擊「🚀 開始比對」按鈕
        - 等待處理完成（會顯示進度條和狀態）
        - 處理時間依檔案大小而定
        
        **步驟 4：下載結果**
        - 比對完成後，會出現「📥 下載比對結果 Excel」按鈕
        - 點擊下載，檔案會自動儲存
        - 檔案名稱格式：`EPA_比對結果_YYYYMMDD_HHMMSS.xlsx`
        """)
    
    st.markdown("---")
    st.header("⚠️ 注意事項")
    st.markdown("""
    ✅ **檔案要求**
    - 至少需要 **2 個檔案**才能進行比對
    - 檔案必須包含 **Project Name** 或 **Applicant Name** 欄位
    - 建議所有檔案的欄位結構保持一致
    
    📅 **時間判斷**
    - 檔案會依修改時間自動排序（舊 → 新）
    - 如需手動指定日期，請使用命令列版本
    
    🔒 **資料安全**
    - 上傳的檔案僅在處理時暫存
    - 處理完成後自動清除
    - 不會儲存您的原始資料
    """)
    
    st.markdown("---")
    st.header("💡 顏色說明")
    
    st.markdown("**🟡 黃色標示**")
    st.markdown("""
    - 最新時間點與前一個時間點相比，欄位值有差異
    - 標記範圍：變動的儲存格 + Seq + Snapshot_Date + 專案名稱
    - 目的：快速識別有變動的專案
    """)
    
    st.markdown("**🔴 紅色標示**")
    st.markdown("""
    - 不同檔案的欄位結構不一致
    - 可能原因：欄位數量、名稱、順序不同
    - 處理：檢查資料來源，確保結構一致
    """)
    
    st.markdown("---")
    st.caption("💬 需要幫助？查看 README_STREAMLIT.md")

# 主內容區
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📁 檔案上傳")
    
    # 檔案上傳器
    uploaded_files = st.file_uploader(
        "選擇 Excel 檔案（可多選）",
        type=['xlsx', 'xls'],
        accept_multiple_files=True,
        help="請選擇 2 個或以上的 Excel 檔案進行比對"
    )

# 顯示上傳的檔案資訊
if uploaded_files:
    st.markdown("---")
    st.header("📋 已上傳的檔案")
    
    # 建立檔案資訊列表
    file_info = []
    for idx, file in enumerate(uploaded_files, start=1):
        file_size = len(file.getvalue()) / 1024  # KB
        # 取得檔案修改時間（從檔案名稱或使用當前時間）
        try:
            # 嘗試從檔案名稱提取日期
            mod_time = "自動判斷"
        except:
            mod_time = "自動判斷"
        
        file_info.append({
            '序號': idx,
            '檔案名稱': file.name,
            '檔案大小': f"{file_size:.2f} KB",
            '檔案類型': file.type or 'application/vnd.ms-excel',
            '處理狀態': '✅ 已就緒'
        })
    
    df_files = pd.DataFrame(file_info)
    st.dataframe(df_files, use_container_width=True, hide_index=True)
    
    # 顯示檔案總數和總大小
    total_size = sum(len(f.getvalue()) for f in uploaded_files) / 1024 / 1024  # MB
    st.caption(f"📊 總計：{len(uploaded_files)} 個檔案，總大小：{total_size:.2f} MB")
    
    # 檢查檔案數量
    if len(uploaded_files) < 2:
        st.warning("⚠️ 至少需要上傳 2 個 Excel 檔案才能進行比對！")
    else:
        st.success(f"✅ 已上傳 {len(uploaded_files)} 個檔案，可以開始比對")
        
        # 比對按鈕
        st.markdown("---")
        col_btn1, col_btn2 = st.columns([1, 4])
        
        with col_btn1:
            if st.button("🚀 開始比對", type="primary", use_container_width=True):
                # 初始化進度條
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # 建立臨時目錄儲存上傳的檔案
                    with tempfile.TemporaryDirectory() as temp_dir:
                        temp_files = []
                        
                        status_text.text("📂 正在儲存上傳的檔案...")
                        progress_bar.progress(10)
                        
                        # 儲存所有上傳的檔案到臨時目錄
                        for idx, uploaded_file in enumerate(uploaded_files):
                            # 確保檔案名稱唯一（避免重複名稱）
                            safe_name = f"{idx+1}_{uploaded_file.name}"
                            temp_path = os.path.join(temp_dir, safe_name)
                            with open(temp_path, 'wb') as f:
                                f.write(uploaded_file.getbuffer())
                            temp_files.append(temp_path)
                            
                            # 更新進度
                            progress = 10 + int((idx + 1) / len(uploaded_files) * 20)
                            progress_bar.progress(progress)
                        
                        status_text.text("🔍 正在執行比對...")
                        progress_bar.progress(30)
                        
                        # 執行比對
                        status_text.text("🔍 正在載入檔案並檢查結構...")
                        progress_bar.progress(40)
                        
                        comparator = EPAProjectComparator(temp_files)
                        
                        status_text.text("📊 正在分析資料並比對變動...")
                        progress_bar.progress(60)
                        
                        # 建立輸出檔案路徑
                        output_filename = f"EPA_比對結果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                        output_path = os.path.join(temp_dir, output_filename)
                        
                        # 執行比對並匯出
                        comparator.compare_and_export(output_path)
                        
                        progress_bar.progress(90)
                        
                        status_text.text("✅ 比對完成！")
                        progress_bar.progress(100)
                        
                        # 讀取結果檔案
                        with open(output_path, 'rb') as f:
                            result_data = f.read()
                        
                        # 儲存到 session state
                        st.session_state['result_data'] = result_data
                        st.session_state['result_filename'] = output_filename
                        st.session_state['comparison_done'] = True
                        
                        st.success("✅ 比對完成！請點擊下方按鈕下載結果。")
                        
                except FileNotFoundError as e:
                    st.error(f"❌ 檔案錯誤：找不到指定的檔案\n{str(e)}")
                    st.session_state['comparison_done'] = False
                except ValueError as e:
                    st.error(f"❌ 資料錯誤：{str(e)}\n\n💡 請確認：\n- 檔案包含 'Project Name' 或 'Applicant Name' 欄位\n- 檔案格式正確")
                    st.session_state['comparison_done'] = False
                except Exception as e:
                    st.error(f"❌ 發生錯誤：{str(e)}")
                    with st.expander("查看詳細錯誤資訊"):
                        st.exception(e)
                    st.session_state['comparison_done'] = False
        
        # 下載按鈕
        if st.session_state.get('comparison_done', False):
            st.markdown("---")
            st.header("📥 下載結果")
            
            result_data = st.session_state.get('result_data')
            result_filename = st.session_state.get('result_filename', 'result.xlsx')
            
            if result_data:
                st.download_button(
                    label="📥 下載比對結果 Excel",
                    data=result_data,
                    file_name=result_filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary",
                    use_container_width=True
                )
                
                st.info("💡 下載的 Excel 檔案包含顏色標記，可用 Excel 或 Google Sheets 開啟查看。")
                
                # 顯示統計資訊（如果有的話）
                if 'comparison_stats' in st.session_state:
                    st.markdown("### 📊 比對統計")
                    st.json(st.session_state['comparison_stats'])

else:
    # 未上傳檔案時的說明
    st.info("👆 請在上方上傳 Excel 檔案開始使用")
    
    st.markdown("---")
    st.header("📚 功能說明")
    
    col_info1, col_info2 = col_info3 = st.columns(3)
    
    col_info1, col_info2, col_info3 = st.columns(3)
    
    with col_info1:
        st.markdown("""
        ### 🎯 主要功能
        - 自動比對多個時間點的 EPA 專案資料
        - 標示實質變動的欄位
        - 檢查欄位結構一致性
        - 自動判斷檔案時間順序
        """)
    
    with col_info2:
        st.markdown("""
        ### 🔍 比對邏輯
        - 使用 **Project Name** 或 **Applicant Name** 識別專案
        - 只比較最新時間點與前一個時間點
        - 避免跨期跳躍比對，減少誤報
        """)
    
    with col_info3:
        st.markdown("""
        ### 📋 輸出內容
        - 新增 **Seq** 欄位（序列號）
        - 新增 **Snapshot_Date** 欄位（資料時間）
        - 保留所有原始欄位
        - 顏色標記變動和異常
        """)

# 頁尾
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "EPA 專案版本比對工具 v1.0 | "
    "專為能源/法規分析師設計"
    "</div>",
    unsafe_allow_html=True
)
