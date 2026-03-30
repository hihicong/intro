
import streamlit as st
import altair as alt
import pandas as pd

st.title('📊 分析結果: 表格/圖表')

# # 初始化 P3 需要嗎？
# if 'result' not in st.session_state:
#     st.session_state['result'] = None
# if 'prev_result' not in st.session_state:
#     st.session_state['prev_result'] = None

if 'show_result_table' not in st.session_state:
    st.session_state['show_result_table'] = True
if 'result' not in st.session_state:
    st.session_state['result'] = None
if 'show_result_chart' not in st.session_state:
    st.session_state['show_result_chart'] = True
if 'chart_type' not in st.session_state:
    st.session_state['chart_type'] = '直方圖'
if 'chart_x' not in st.session_state:
    st.session_state['chart_x'] = '議題'
if 'chart_y' not in st.session_state:
    st.session_state['chart_y'] = 'Engaged views'

# 顯示表格
if st.session_state['result'] is not None:
    st.session_state['show_result_table'] = st.checkbox("顯示表格", value=st.session_state['show_result_table'])
    if st.session_state['show_result_table']:
        st.dataframe(st.session_state['result_table'])

st.divider()

# 顯示圖表
if st.session_state['result'] is not None:
    st.session_state['show_result_chart'] = st.checkbox("顯示圖表", value=st.session_state['show_result_chart'])

    if st.session_state['show_result_chart']:
        df = st.session_state['result_table']
        columns = df.columns.tolist()
        numeric_columns = df.select_dtypes(include='number').columns.tolist()

        st.markdown("### 圖表設定")

        # 圖表類型選單：保留選擇
        chart_type_options = ['直方圖', '其他']
        current_chart_type = st.session_state.get('chart_type', '直方圖')
        st.session_state['chart_type'] = st.selectbox(
            "選擇圖表類型",
            options=chart_type_options,
            index=chart_type_options.index(current_chart_type) if current_chart_type in chart_type_options else 0
        )

        if st.session_state['chart_type'] == '直方圖':
            col1, col2 = st.columns(2)

            # 處理 X 軸選單
            x_current = st.session_state.get('chart_x', columns[0])
            x_index = columns.index(x_current) if x_current in columns else 0
            with col1:
                st.session_state['chart_x'] = st.selectbox("X軸欄位(類別)", options=columns, index=x_index)

            # 處理 Y 軸選單
            y_options = numeric_columns if numeric_columns else columns
            y_current = st.session_state.get('chart_y', y_options[0])
            y_index = y_options.index(y_current) if y_current in y_options else 0
            with col2:
                st.session_state['chart_y'] = st.selectbox("Y軸欄位(數值)", options=y_options, index=y_index)

            x_col = st.session_state['chart_x']
            y_col = st.session_state['chart_y']

            if pd.api.types.is_numeric_dtype(df[y_col]):
                grouped_df = df.groupby(x_col)[y_col].sum().reset_index()
                grouped_df = grouped_df.sort_values(by=y_col, ascending=False)

                # 強制排序分類欄位，防止圖表亂序
                grouped_df[x_col] = pd.Categorical(
                    grouped_df[x_col],
                    categories=grouped_df[x_col],
                    ordered=True
                )

                # 繪製直方圖
                chart = alt.Chart(grouped_df).mark_bar().encode(
                    x=alt.X(f'{x_col}:N', sort=None, title=x_col),
                    y=alt.Y(f'{y_col}:Q', title=y_col),
                    tooltip=[x_col, y_col]
                ).properties(
                    width=600,
                    height=400
                )

                st.altair_chart(chart, use_container_width=True)
            else:
                st.warning(f"Y軸欄位「{y_col}」不是數值型別，無法繪製直方圖。")

        elif st.session_state['chart_type'] == '其他':
            st.info("目前僅支援直方圖，其它圖表類型尚未開放。")

