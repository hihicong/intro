#%%
import streamlit as st

st.title('📕 平台介紹')

tab1, tab2 = st.tabs(["數據來源", "介面介紹"])

with tab1:
    st.markdown(
        """
        <div style='font-size:18px; line-height:1.8'>
        <ol>
            <ol type="a">
                <li>數據來源自YouTube 官方 API。</li>
                <li>因資料蒐集時間點、統計方式及平台更新機制不同，
                    本資料與其他第三方統計結果，可能略有差異，
                    惟不影響整體趨勢與相對表現之分析。</li>
            </ol>
        </ol>
        </div>
        """,
        unsafe_allow_html=True
    )

with tab2:
    st.subheader("1. 流量排名")
    st.markdown(
        """
        <div style='font-size:18px; line-height:1.8'>
        <ol>
            <ol type="a">
                <li>選擇日期</li>
                <li>選擇頻道類別</li>
                <li>排名僅顯示前100名, 可下載完整數據。下載格式: CSV</li>
                <span>註：選擇頻道類別後, 會自動更新數據</span>
            </ol>
        </ol>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.image("user_guide/channel_ranking.png", width=1000)

    st.divider()

    st.subheader("2. 每日流量")

    st.markdown(
        """
        <div style='font-size:18px; line-height:1.8'>
        <ol>
            <ol type="a">
                <li>選擇日期</li>
                <li>選擇頻道</li>
                <li>可下載完整數據。下載格式: CSV</li>
                <span>註：選擇頻道後, 會自動更新數據</span>
            </ol>
        </ol>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.image("user_guide/daily.png", width=1000)

    st.divider()

    st.subheader("3. 影片流量")

    st.markdown(
        """
        <div style='font-size:18px; line-height:1.8'>
        <ol>
            <ol type="a">
                <li>選擇日期</li>
                <li>選擇頻道類別</li>
                <li>選擇頻道</li>
                <li>選擇影片類型</li>
                <li>點擊查詢</li>
                <li>點擊進行AI内容分析</li>
                <li>排名僅顯示前50名, 可下載完整數據。下載格式: CSV</li>
            </ol>
        </ol>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.image("user_guide/video_view.png", width=1000)




