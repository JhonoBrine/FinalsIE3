import streamlit as st
import os


st.image("assets/image/BAOBAO.png")

members = [
    {"name": "Gil Joshua Yabao", "image": "assets/image/joshua.jpg", "role": "Leader"},
    {"name": "Jhon Lorenz Pabroa", "image": "assets/image/pabs.jpg", "role": "Member"},
    {"name": "Rey Dante Garcia", "image": "assets/image/rey.jpg", "role": "Member"},
    {"name": "Trisha Mae Rivera", "image": "assets/image/trisha.jpg", "role": "Member"},
    {"name": "Mark Edwin Huyo-a", "image": "assets/image/mark.jpg", "role": "Member"},
]

leader = next(member for member in members if member["role"] == "Leader")

st.markdown("<h2 style=' color: white;'>Team Leader</h2>", unsafe_allow_html=True)
leader_col = st.container()
with leader_col:
    st.image(leader["image"], width=200, caption=f"{leader['name']}")

st.write("")
st.markdown("<h2 style='color: white;'>Members</h2>", unsafe_allow_html=True)
columns = st.columns(2)

for i, member in enumerate(members):
    if member["role"] == "Member":
        with columns[i % 2]:
            st.image(member["image"], width=200, caption=f"{member['name']}")
