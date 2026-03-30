#%%
import streamlit as st

st.title('📕 系統介紹')

tab1, tab2, tab3 = st.tabs(["使用須知", "使用流程", "模型介紹"])

with tab1:
    # st.markdown(
    #     """
    #     <div style='font-size:18px; line-height:1.8'>
    #     <ol>
    #         <li>資料隱私與保密性
    #             <ol type="a">
    #                 <li>切勿輸入機密資料（如個資、收益）</li>
    #                 <li>若要使用敏感數據，請進行匿名化或加密</li>
    #             </ol>
    #         </li>

    #         <li>AI 分析的準確性與可靠性
    #             <ol type="a">
    #                 <li>AI 可能產生不準確或不符預期的內容</li>
    #                 <li>建議由人工進行審核，以確保生成內容的準確性與一致性</li>
    #                 <li>請勿在未經審核的情況下，直接使用 AI 分析結果</li>
    #             </ol>
    #         </li>

    #         <li>數據品質
    #             <ol type="a">
    #                 <li>在輸入資料前，請先進行資料清理，避免缺失值、錯誤格式或極端值影響 AI 判斷</li>
    #                 <li>數據輸入的長度會影響 AI 的分析時間。資料量越大，所需分析時間越長</li>
    #             </ol>
    #         </li>
    #     </ol>
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )

    st.markdown(
        """
        <style>
        ol { font-size: 18px; line-height: 1.8; }
        ol ol { list-style-type: lower-alpha; margin-left: 20px; }
        </style>
        <ol>
            <li>資料隱私與保密性
                <ol>
                    <li>切勿輸入機密資料（如個資、收益）</li>
                    <li>若要使用敏感數據，請進行匿名化或加密</li>
                </ol>
            </li>
            <li>AI 分析的準確性與可靠性
                <ol>
                    <li>AI 可能產生不準確或不符預期的內容</li>
                    <li>建議由人工進行審核，以確保生成內容的準確性與一致性</li>
                    <li>請勿在未經審核的情況下，直接使用 AI 分析結果</li>
                </ol>
            </li>
            <li>數據品質
                <ol>
                    <li>在輸入資料前，請先進行資料清理，避免缺失值、錯誤格式或極端值影響 AI 判斷</li>
                    <li>數據輸入的長度會影響 AI 的分析時間。資料量越大，所需分析時間越長</li>
                </ol>
            </li>
        </ol>
        """,
        unsafe_allow_html=True
    )


with tab2:
    st.subheader("1. 上傳檔案")
    st.markdown(
        """
        <div style='font-size:18px; line-height: 1.8'>
        <ol>
            <li>在工具表中選擇上傳檔案</li>
            <li>點擊上傳檔案</li>
            <li>選擇文件</li>
            <span>註：僅支援CSV或Excel格式</span>
        </ol>  
        </div>
        """,
        unsafe_allow_html=True
    )
    st.image("user_guide/upload_file.png", width=1000)
    st.image("user_guide/choose_file.png", width=1000)

    st.divider()

    st.subheader("2. 分析設定")

    st.markdown(
        """
        <div style='font-size:18px; line-height: 1.8'>
        <ol>
            <li>在工具表中選擇GenAI分析</li>
            <li>選擇分析模型</li>
            <li>選擇資料量<br><span style='color:white; font-size:16px;'>註：資料量越大，分析所需時間越長</span></li>
            <li>選擇分析指標</li>
            <li>選擇欄位<br>
                <span style='color:white; font-size:16px;'>註1：爲確保隱私權，請不要選擇有關個人資料以及收益相關的欄位</span><br>
                <span style='color:white; font-size:16px;'>註2：欄位數量越多，分析所需時間越長</span><br>
                <span style='color:white; font-size:16px;'>註3：index 以及 影片標題 為必要欄位</span>
            </li>
            <li>輸入提示詞<br>
                <span style='color:white; font-size:16px;'>註1：已有預設提示詞，可不輸入</span><br>
                <span style='color:white; font-size:16px;'>註2：可根據分析結果，輸入更多要求/span><br>
                <span style='color:white; font-size:16px;'>例如：將 Shorts 進行獨立說明</span>
            </li>
            <li>執行分析</li>
        </ol>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.image("user_guide/setting.png", width=1000)

    st.divider()

    st.subheader("3. 下載分析結果")

    st.markdown(
        """
        <div style='font-size:18px; line-height: 1.8'>
        <ol>
            <li>點擊下載分析結果</li>
            <li>選擇信任文件</li>
            <span>註：輸出文件格式為PDF</span>
        </ol>  
        </div>
        """,
        unsafe_allow_html=True
    )

    st.image("user_guide/download_text_result.png", width=1000)
    st.image("user_guide/trust_text_result.png", width=400)

    st.divider()

    st.subheader("4. 查看分析結果: 表格/圖表")

    st.markdown(
        """
        <div style='font-size:18px; line-height: 1.8'>
        <ol>
            <li>在工具表中選擇分析結果: 表格/圖表</li>
            <li>下載表格<br>
                <span>a. ：可將下載後的表格進行後續的樞紐分析</span><br>
                <span>註1：註1：請人工檢核資料是否正確</span><br>
                <span>註2：註2：輸出文件格式為CSV</span>
            </li>
            <li>下載圖表<br>
                <ol type="a">
                <li>選擇圖表類型</li>
                <li>選擇x軸(類別)</li>
                <li>選擇y軸(數值)</li> 
                <li>點擊更多(...)</li> 
                <li>選擇儲存格式</li> 
                </ol>
            </li>   
        </ol>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.image("user_guide/result_table.png", width=1000)
    st.image("user_guide/download_png_result.png", width=1000)

with tab3:

    # 圖表類型選單：保留選擇
    model_options = ['AI議題分析', '其他']
    model = st.selectbox(
        "選擇模型",
        options=model_options
    )

    if model == "AI議題分析":
        st.markdown(
        """
        <div style='font-size:18px; line-height: 1.8'>
        <span>功能：將影片標題分析成不同的議題</span><br>
        <span>適用範圍：YT/抖音</span><br>
        <span>必要欄位：影片標題</span><br>
        <span>模型説明：</span><br>
        <ol>
        <li>該模型使用Gemini 進行議題分析 (不進行任何統計計算)</li>
        <li>使用python進行樞紐分析 (進行統計計算)</li>
        </ol>
        <span>輸出結果説明</span><br>
        <ol>
            <li>議題</li>
            <li>主要關鍵人物</li>
            <li>主要國家/地區</li>
            <li>主題</li>
            <li>説明文</li>
            <li>指標</li>
            <li>影片數</li>
        </ol> 
        </div>
        """,
        unsafe_allow_html=True
        )
        
    elif model == "其他":
        st.markdown("### 無説明")
