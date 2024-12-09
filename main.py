import streamlit as st
import os

thisfile = os.path.abspath(__file__)
base_dir = os.path.dirname(thisfile)

file = os.path.join(base_dir, "views/introductionPage.py")

# -- PAGE SETUP --

# Introduction Page
## This is the page that we will introduce the Grocery dataset that will be used on the dataPage.py. Most simple tables and explanations regarding
## Apriori Algorithm will be explained here, should be concise and be able to explain the graphs properly.

home_page = st.Page(
    page="views/introductionPage.py",
    title="Introduction",
    icon=":material/home:",
    default=True,
)

data_page = st.Page(
    page="views/dataPage.py",
    title="Introduction",
    icon=":material/home:",
)

member_page = st.Page(
    page="views/membersPage.py",
    title="Introduction",
    icon=":material/home:",
)


# NAVIGATION SETUP
pg = st.navigation(
    {
        "Home": [home_page],
        "Data Visualization": [data_page],
        "BaoBao": [member_page],
    }
)



# SHARED ON ALL PAGES
st.logo("assets/image/BAOBAO.png")
st.sidebar.text("For CSIT342 - Industry Elective 3")


# RUN NAVIGATION
pg.run()
