#%%
import streamlit as st
import toml

def main():
    st.set_page_config(page_title="專案介紹", page_icon="💻")

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