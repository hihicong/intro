#%%
import streamlit as st
#from ST_menu import menu
from io import StringIO
import pandas as pd
import toml
import importlib.util

def main():
    st.set_page_config(page_title="AI應用分析", page_icon="✨")

    config = toml.load(".streamlit/pages.toml")

    pages = [
        st.Page(
            page["path"],
            title=page["name"],
            icon=page.get("icon", None)
        )
        for page in config["pages"]
    ]

    pg = st.navigation(pages)
    pg.run()


if __name__ == '__main__':
    # menu()
    main()