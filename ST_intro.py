#%%
import streamlit as st
#from ST_menu import menu
from gemini_analysis import Genai
from io import StringIO
import pandas as pd
import toml
import importlib.util
from st_pages import add_page_title, get_nav_from_toml




def main():
    st.set_page_config(
        page_title="AI應用分析",
        page_icon="✨")

    # 讀取整個 config
    nav = get_nav_from_toml(".streamlit/pages.toml")
    pg = st.navigation(nav)
    # add_page_title(nav)
    pg.run()


if __name__ == '__main__':
    # menu()
    main()