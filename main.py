import streamlit as st
import os

thisfile = os.path.abspath(__file__)
base_dir = os.path.dirname(thisfile)

file = os.path.join(base_dir, "views/introductionPage.py")

# -- PAGE SETUP --

# Introduction Page
## This is the page that we will introduce the Grocery dataset that will be used on the dataPage.py. Most simple tables and explanations regarding
## Apriori Algorithm will be explained here, should be concise and be able to explain the graphs properly. The cleaning will be mentioned here, and 
## the process of the cleaning will be mentioned here.

home_page = st.Page(
    page="views/introductionPage.py",
    title="Introduction",
    icon=":material/home:",
    default=True,
)


# Data Page
## This is the page where most of the graphs, with different possible combinations used for Apriori Algorithm is up. Explanations for each data will be here...
## no tables or few tables will only be available here, since only graphs that are related to Grocery dataset should be here. Data cleaning should only happen in the background
data_page = st.Page(
    page="views/dataPage.py",
    title="Grocery Dataset by transaction",
    icon=":material/home:",
)

data_page_2 = st.Page(
    page="views/dataPage2.py",
    title="Grocery Dataset by members",
    icon=":material/home:",
)

data_test_page = st.Page(
    page="views/testPage.py",
    title="Test Dataset",
    icon=":material/home:",
)

conc_reco_page = st.Page(
    page="views/conclusionNRecommendationPage.py",
    title="Conclusion and Recommendation",
    icon=":material/home:",
)

# Members Page
## Self explanatory
member_page = st.Page(
    page="views/membersPage.py",
    title="Bao Bao",
    icon=":material/home:",
)


# NAVIGATION SETUP
pg = st.navigation(
    {
        "Home": [home_page],
        "Data Visualization": [data_page,data_page_2, data_test_page],
        "Finale": [conc_reco_page],
        "BaoBao": [member_page],
    }
)



# SHARED ON ALL PAGES
st.logo("assets/image/BAOBAO.png")
st.sidebar.text("For CSIT342 - Industry Elective 3")


# RUN NAVIGATION
pg.run()
