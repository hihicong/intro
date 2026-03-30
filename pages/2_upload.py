import streamlit as st
import pandas as pd
from io import BytesIO

st.title("📂 上傳檔案")

# 初始化 session_state
if 'file_bytes' not in st.session_state:
    st.session_state['file_bytes'] = None
if 'filename' not in st.session_state:
    st.session_state['filename'] = None
if 'df' not in st.session_state:
    st.session_state['df'] = None
if 'sheet_name' not in st.session_state:
    st.session_state['sheet_name'] = None
if 'show_df' not in st.session_state:
    st.session_state['show_df'] = True

uploaded_file = st.file_uploader("請上傳 CSV 或 Excel 檔案", type=["csv", "xls", "xlsx"])

# 顯示檔案名稱以及清除按鈕
if uploaded_file is None and st.session_state.get('filename'):
    col1, col2 = st.columns([4,1])
    with col1:
        st.markdown(
            f"""
            <div style="margin-top: 8px; align-items: center; height: 100%;font-size: 20px;">
                <strong>目前上傳的檔案：</strong> <code>{st.session_state['filename']}</code>
            </div>
            """,
            unsafe_allow_html=True
        )
    # st.markdown(f"**目前上傳的檔案：** `{st.session_state['filename']}`")
    with col2:
        if st.button("❌", help = "清除上傳檔案"):
            st.session_state['file_bytes'] = None
            st.session_state['filename'] = None
            st.session_state['df'] = None
            st.session_state['sheet_name'] = None
            st.session_state['show_df'] = True
            st.rerun()

# 檔案上傳設定
if uploaded_file is not None:
    try:
        # 儲存檔案資訊到 session_state
        file_bytes = uploaded_file.read()
        st.session_state['file_bytes'] = file_bytes
        st.session_state['filename'] = uploaded_file.name

        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(BytesIO(file_bytes))
            st.session_state['df'] = df
            st.session_state['sheet_name'] = None

        else:
            all_sheets = pd.read_excel(BytesIO(file_bytes), sheet_name=None)
            sheet_names = list(all_sheets.keys())

            saved_sheet = st.session_state.get('sheet_name')
            if saved_sheet not in sheet_names:
                saved_sheet = sheet_names[0]
                st.session_state['sheet_name'] = saved_sheet

            selected_sheet = st.selectbox("請選擇要工作表", sheet_names, index=sheet_names.index(saved_sheet))
            st.session_state['sheet_name'] = selected_sheet
            df = all_sheets[selected_sheet]
            st.session_state['df'] = df

    except Exception as e:
        st.error(f"處理 {uploaded_file.name} 時發生錯誤：{e}")

# 若是重新回來這頁，session 有資料就自動顯示
elif st.session_state['file_bytes'] is not None:
    try:
        filename = st.session_state['filename']
        file_bytes = st.session_state['file_bytes']

        if filename.endswith('.csv'):
            df = pd.read_csv(BytesIO(file_bytes))
            st.session_state['df'] = df

        else:
            all_sheets = pd.read_excel(BytesIO(file_bytes), sheet_name=None)
            sheet_names = list(all_sheets.keys())

            selected_sheet = st.selectbox("請選擇要工作表", sheet_names, index=sheet_names.index(st.session_state['sheet_name']))
            st.session_state['sheet_name'] = selected_sheet
            df = all_sheets[selected_sheet]
            st.session_state['df'] = df

    except Exception as e:
        st.error(f"重新載入 {filename} 時發生錯誤：{e}")

# 顯示表格
if st.session_state['df'] is not None:
    st.session_state['show_df'] = st.checkbox("顯示表格", value=st.session_state['show_df'])
    if st.session_state['show_df']:
        st.write(st.session_state['df'])




#####################################################################################
# # 上傳文件
# uploaded_file = st.file_uploader("請上傳你的文件", type=["csv", "xlsx"])

# if uploaded_file is not None:
#     try:
#         if uploaded_file is not None:
            
#             if uploaded_file.name.endswith('.csv'):
#                 df = pd.read_csv(uploaded_file)

#             else:
#                 all_sheets = pd.read_excel(uploaded_file, sheet_name=None)
#                 sheet_names = list(all_sheets.keys())
#                 selected_sheet = st.selectbox("請選擇要工作表", sheet_names)
#                 df = all_sheets[selected_sheet]

#             st.session_state['df'] = df
            
#             show_df = st.checkbox("Show table", value=True)
#             if show_df:
#                 st.write(df)
        
#     except Exception as e:
#         st.error(f"處理{uploaded_file.name}時發生錯誤：{e}")


