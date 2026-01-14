#!/bin/bash
# EPA 專案比對工具啟動腳本

echo "🚀 啟動 EPA 專案版本比對工具..."
echo ""

# 檢查是否已安裝依賴
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "⚠️  檢測到缺少依賴套件，正在安裝..."
    pip install -r requirements.txt
    echo ""
fi

# 啟動 Streamlit 應用
echo "📊 正在啟動網頁介面..."
echo "🌐 瀏覽器將自動開啟，或手動訪問：http://localhost:8501"
echo ""
echo "按 Ctrl+C 可停止服務"
echo ""

streamlit run app.py
