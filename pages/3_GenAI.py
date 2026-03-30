import streamlit as st
from gemini_analysis import Genai
import pandas as pd
import time
from tool import JsonParse, PDFExporter

st.title("🧠 GenAI分析")

# 初始化 session_state P2
if 'file_bytes' not in st.session_state:
    st.session_state['file_bytes'] = None
if 'filename' not in st.session_state:
    st.session_state['filename'] = ''
if 'df' not in st.session_state:
    st.session_state['df'] = None
if 'sheet_name' not in st.session_state:
    st.session_state['sheet_name'] = None
if 'show_df' not in st.session_state:
    st.session_state['show_df'] = True

# 初始化 session_state P3
if 'model' not in st.session_state:
    st.session_state['model'] = None
if 'data_size' not in st.session_state:
    st.session_state['data_size'] = None
if 'metric' not in st.session_state:
    st.session_state['metric'] = None
if 'prev_metric' not in st.session_state:
    st.session_state['prev_metric'] = []
if 'df_column' not in st.session_state:
    st.session_state['df_column'] = None
if 'prev_columns' not in st.session_state:
    st.session_state['prev_columns'] = []
if 'result' not in st.session_state:
    st.session_state['result'] = None
if 'elapsed_time' not in st.session_state:
    st.session_state['elapsed_time'] = 0
if 'candidates_token_count' not in st.session_state:
    st.session_state['candidates_token_count'] = 0
if 'prompt_token_count' not in st.session_state:
    st.session_state['prompt_token_count'] = 0
if 'total_output_token' not in st.session_state:
    st.session_state['total_output_token'] = 0
if 'total_input_token' not in st.session_state:
    st.session_state['total_input_token'] = 0
if 'prev_filename' not in st.session_state:
    st.session_state['prev_filename'] = None
if 'prev_sheetname' not in st.session_state:
    st.session_state['prev_sheetname'] = None

filename = st.session_state.get('filename')
sheet_name = st.session_state.get('sheet_name')

# 判斷是否需要初始化
is_new_data = (
    filename != st.session_state['prev_filename'] or
    sheet_name != st.session_state['prev_sheetname'] or
    filename is None or
    (sheet_name is None and 'sheetname' in st.session_state)  # 明確設為 None
)

if is_new_data:
    # 更新紀錄
    st.session_state['prev_filename'] = filename
    st.session_state['prev_sheetname'] = sheet_name

    # 初始化分析相關狀態
    st.session_state['result'] = None
    st.session_state['elapsed_time'] = 0
    st.session_state['candidates_token_count'] = 0
    st.session_state['prompt_token_count'] = 0
    st.session_state['total_output_token'] = 0
    st.session_state['total_input_token'] = 0
    st.session_state['metric'] = None
    st.session_state['df_column'] = None
    st.session_state['prev_columns'] = []

# 顯示檔案名稱以及清除按鈕
if filename:
    col1, col2 = st.columns([4,1])
    with col1:
        st.markdown(
            f"""
            <div style="margin-top: 8px; align-items: center; height: 100%;font-size: 20px;">
                <strong>目前上傳的檔案：</strong> <code>{filename}</code>{f":<code>{sheet_name}</code>" if sheet_name else ""}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        if st.button("❌", help = "清除上傳檔案"):
            st.session_state['file_bytes'] = None
            st.session_state['filename'] = None
            st.session_state['df'] = None
            st.session_state['sheet_name'] = None
            st.session_state['show_df'] = True
            # st.session_state['result'] = None
            st.rerun()
        
else:
    st.warning("尚未上傳資料，若有需請到上頁上傳檔案。")

# GenAI 設定
api_key="AIzaSyCUsfrfANDslM2myifVOrEonHFpKhOV2Vc"
# "AIzaSyCUsfrfANDslM2myifVOrEonHFpKhOV2Vc", "AIzaSyBxaTpzecewH9fpsAzfYIEJBsHYpzbfQBo" my #'AIzaSyAQN2j_TIb5_oD0QsZwcWOTqLwvDT8og1E' andrew

GenAI = Genai(api_key)

# 選擇模型
model_options = ['AI議題分析', '模型B (建制中)', '模型C (建制中)', '模型D (建制中)']

if st.session_state['model'] not in model_options:
    st.session_state['model'] = model_options[0]

model = st.selectbox(
    '請選擇分析模型',
    model_options,
    index=model_options.index(st.session_state['model'])
)

st.session_state['model'] = model

# 設置column 
if 'df' in st.session_state and st.session_state['df'] is not None:
    df = st.session_state['df']
    col0 = df.columns[0]
    df = df[~df[col0].isin(["Total", "Showing top 500 results", "總計", "目前顯示最熱門的 500 項結果"])]

    # 資料量
    df_len = len(df)
    percentage_values = [0.25, 0.5, 0.75, 1.0]

    data_size_option = [f"{int(p * 100)}% 資料量 ({int(df_len * p)} 筆)" for p in percentage_values]

    if 'data_size' not in st.session_state or st.session_state['data_size'] not in data_size_option:
        st.session_state['data_size'] = data_size_option[0]

    data_size = st.selectbox(
        '請選擇資料量',
        options=data_size_option,
        index=data_size_option.index(st.session_state['data_size']))
    
    st.session_state['data_size'] = data_size

    selected_index = data_size_option.index(data_size)
    selected_percentage = percentage_values[selected_index]

    rows_to_show = int(len(df) * selected_percentage)
    Json_df = df.head(rows_to_show)
    
    # 移除收益
    Json_df.insert(0, 'index_no', range(1, len(Json_df) + 1))
    result_df = Json_df
    filtered_df = result_df.loc[:, ~result_df.columns.str.contains('revenue|收益', case=False, regex=True)]

    # 指標
    columns = filtered_df.columns.tolist()
    is_new_file_metric = st.session_state['prev_metric'] != columns
    st.session_state['prev_metric'] = columns

    if is_new_file_metric:
        default_metric = [col for col in columns if '互動觀看次數' in col or 'Engaged views' in col]
        st.session_state['metric'] = default_metric[0] if default_metric else columns[0]
    else:
        if 'metric' not in st.session_state or st.session_state['metric'] not in columns:
            default_metric = [col for col in columns if '互動觀看次數' in col or 'Engaged views' in col]
            st.session_state['metric'] = default_metric[0] if default_metric else columns[0]

    default_index = columns.index(st.session_state['metric'])

    selected_metric = st.selectbox(
        '請選擇要分析的指標：',
        options=columns,
        index=default_index)

    st.session_state['metric'] = selected_metric

    if selected_metric in ["Content", "Video title", "内容", "影片標題"]:
        st.warning("請選擇分析指標")
        st.stop()

    # 多選欄位
    columns = filtered_df.columns.tolist()

    is_new_file = st.session_state['prev_columns'] != columns
    st.session_state['prev_columns'] = columns
    
    default_columns = ['index_no']
    default_columns += [col for col in filtered_df if '影片標題' in col or 'Video title' in col]
    if len(default_columns) == 1:  # 只加了 df_index，沒找到其他的
        default_columns = columns

    if is_new_file:
        valid_selected_columns = default_columns
    else:
        valid_selected_columns = [
            col for col in (st.session_state['df_column'] or []) if col in columns
        ]

        if not valid_selected_columns:
            valid_selected_columns = default_columns

    selected_columns = st.multiselect(
        '請選擇要欄位 (可多選): ',
        options=columns,
        default=valid_selected_columns
    )

    st.session_state['df_column'] = selected_columns

    df_prompt_use = filtered_df[selected_columns]
    df_string = df_prompt_use.to_string()


# 設定一個可以按enter執行的form
with st.form("prompt_form", clear_on_submit=False):
    if model == "AI議題分析":
        user_input = st.text_input(
            "請輸入提示詞 (已有預設提示詞, 可不輸入)",
            "結合時事, 根據video title 分析有什麽主要議題, 單個議題最多涵蓋2個國家或主題。可以細分成多個議題"
        )
    elif model == "模型B (建制中)":
        user_input = st.text_input(
            "請輸入提示詞 (已有預設提示詞, 可不輸入)",
            "模型建制中"
        )

    submitted = st.form_submit_button("執行")

# 設定最終prompt prompt+df
if 'df' in st.session_state and st.session_state['df'] is not None:
    # df = st.session_state['df']

    final_prompt = f"""

    【目標】:
    {user_input}

    【資料内容】
    {df_string}

    """

# 按鈕(enter)操作：調用GenAI
if submitted:
    with st.spinner("分析中，請稍後..."):
        st.divider()
        start_time = time.time()

        # 使用者可手動修改提示詞，這裡傳給 GenAI
        if model == "AI議題分析":
            with open("sys_instruction/model1.txt", "r", encoding="utf-8") as file:
                instruction = file.read()

            attempt = 0
            text = None
            while attempt < 3:
                text, token  = GenAI.analytics(final_prompt, instruction)
                result_text = JsonParse.analyze_and_format(
                    response_text=text,
                    df=Json_df,
                    col=selected_metric,             # <- 你想用的原始欄位
                    agg_col_name=selected_metric,     # <- 你想顯示的名稱
                    use_streamlit= True             # <- 是否在 Streamlit 顯示錯誤
                )
                if result_text:
                    break 
                else:
                    st.warning(f"⚠️ 第 {attempt + 1} 次 JSON 分析失敗，嘗試重跑...")
                    attempt += 1

            if result_text:
                st.session_state['result'] = result_text

            else:
                st.error("❌ 多次嘗試仍失敗，請重新執行或檢查模型輸出格式。")
                st.session_state['result'] = None

        elif model == "模型B (建制中)":
            text, token  = GenAI.analytics(final_prompt)
            st.text(text)

        # 輸出所需時間以及token
        end_time = time.time()  # 记录结束时间
        elapsed_time = end_time - start_time  # 计算运行时间
        st.session_state['elapsed_time'] = round(elapsed_time)
        st.session_state['candidates_token_count'] = token.candidates_token_count
        st.session_state['prompt_token_count'] = token.prompt_token_count
        st.session_state['total_output_token'] = GenAI.token("output")
        st.session_state['total_input_token'] = GenAI.token("input")
        # st.session_state['candidates_token_count'] = 0
        # st.session_state['prompt_token_count'] = 0
        # st.session_state['total_output_token'] = 0
        # st.session_state['total_input_token'] = 0
        # col1, col2, col3 = st.columns(3)
        # with col1:
        #     st.text(f"\n运行时间: {round(elapsed_time)} 秒")
        # with col2:
        #     st.text(f"回應耗用 Token 數: {token.candidates_token_count}")
        # with col3:
        #     st.text(f"提示詞耗用 Token 數: {token.prompt_token_count}")
        # col1, col2, col3 = st.columns(3)
        # with col1:
        #     st.text(f"")
        # with col2:
        #     st.text(f"總回應 Token 數: {GenAI.token("output")}")
        # with col3:
        #     st.text(f"總提示詞 Token 數: {GenAI.token("input")}")

# 最終結果呈現
if 'df' in st.session_state and st.session_state['df'] is not None:
    if 'result' in st.session_state and st.session_state['result'] is not None:


        # if st.button("下載分析結果"):
        #     pdf_data = st.session_state['result']
        #     PDFExporter.generate_pdf(pdf_data)
        #     st.success("Generated example.pdf!")

        # if st.button("下載分析結果"):
        #     pdf_data = st.session_state['result']
        #     pdf_stream = PDFExporter.generate_pdf(pdf_data)
        #     st.download_button(
        #         label="📥 下載 PDF",
        #         data=pdf_stream,
        #         file_name="測試",
        #         mime="application/pdf"
        #     )
        #     st.success("Generated example.pdf!")
        pdf_data = PDFExporter.generate_pdf(st.session_state['result'])
        if st.download_button("下載分析結果", pdf_data, "AI_Analysis_Report.pdf", mime='application/pdf'):
            st.success("已完成下載!")

        # pdf_data = PDFExporter.generate_pdf(st.session_state['result'])
        # st.download_button("下載分析結果", pdf_data, "AI_Analysis_Report.pdf", mime='application/pdf')
        st.text(st.session_state['result'])
    st.divider()

    # 顯示
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text(f"\n运行时间: {st.session_state['elapsed_time']} 秒")
    with col2:
        st.text(f"回應耗用 Token 數: {st.session_state['candidates_token_count']}")
    with col3:
        st.text(f"提示詞耗用 Token 數: {st.session_state['prompt_token_count']}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.text(f"")
    with col2:
        st.text(f"總回應 Token 數: {st.session_state['total_output_token']}")
    with col3:
        st.text(f"總提示詞 Token 數: {st.session_state['total_input_token']}")