"""
Bowtie Diagram Application
Main entry point for the Streamlit application
"""
import streamlit as st
from streamlit.components.v1 import html
from components.html_template import get_html_template

st.set_page_config(
    page_title="Bow-tie (ReactFlow + Auto-layout)", 
    layout="wide"
)

st.title("Bow-tie — ReactFlow inside Streamlit")

# Render the React application
html(
    get_html_template(),
    height=650,
    scrolling=False
)