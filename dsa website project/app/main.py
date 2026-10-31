"""Streamlit entry point for the expense tracker."""

import streamlit as st

from config.settings import APP_NAME
from service.expenses import add_expense, load_expenses
from pages.dashboard import render_dashboard
from pages.expense_list import render_expense_list
from pages.expense_form import render_expense_form

st.set_page_config(page_title=APP_NAME, page_icon="💸", layout="wide", initial_sidebar_state="expanded")

if "expenses" not in st.session_state:
    st.session_state.expenses = load_expenses()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&display=swap');
:root { --ink:#202b32; --muted:#58666d; --line:#dce3e4; --paper:#f5f7f6; --green:#1d674f; --red:#df514b; }
.stApp { background:var(--paper); color:var(--ink); font-family:'DM Sans',sans-serif; }
[data-testid="stAppViewContainer"], [data-testid="stMain"] { color:var(--ink); }
[data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li, [data-testid="stMarkdownContainer"] strong,
[data-testid="stHeader"] { color:var(--ink); }
[data-testid="stWidgetLabel"] p, label, [data-testid="stCaptionContainer"] p,
[data-testid="stMetricLabel"] { color:#46545b !important; }
[data-testid="stCaptionContainer"] p { opacity:1 !important; }
[data-testid="stSidebar"] { background:#eaf0ed; border-right:1px solid var(--line); }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:#46545b; }
[data-testid="stSidebar"] [data-testid="stRadio"] label,
[data-testid="stSidebar"] [data-testid="stRadio"] p { color:var(--ink) !important; }
.brand { font-family:'DM Mono',monospace; font-size:14px; font-weight:500; letter-spacing:-.4px; padding:9px 0 20px; }
.brand span { color:var(--green); }
.eyebrow { color:var(--green); text-transform:uppercase; font:500 11px 'DM Mono',monospace; letter-spacing:1.5px; }
.hero-title { font-size:34px; line-height:1.15; font-weight:600; letter-spacing:-1.2px; margin:4px 0 5px; }
.subtle { color:var(--muted); font-size:14px; }
.panel { background:#fff; border:1px solid var(--line); border-radius:14px; padding:20px 22px; }
.metric-label { color:var(--muted); font:11px 'DM Mono',monospace; text-transform:uppercase; letter-spacing:1px; }
.metric-value { font-size:27px; font-weight:600; letter-spacing:-.7px; margin-top:7px; }
.small-note { color:var(--muted); font-size:12px; margin-top:4px; }
div[data-testid="stMetric"] { background:#fff; border:1px solid var(--line); padding:17px 19px; border-radius:13px; }
div[data-testid="stMetricLabel"] { font:11px 'DM Mono',monospace; text-transform:uppercase; letter-spacing:.9px; color:#46545b !important; }
div[data-testid="stMetricValue"] { font-size:26px; color:var(--ink) !important; }
input, textarea, [data-baseweb="select"] > div, [data-baseweb="input"] > div,
[data-baseweb="select"] input, [data-baseweb="input"] input { color:var(--ink) !important; background-color:#fff !important; }
input::placeholder, textarea::placeholder { color:#68767d !important; opacity:1 !important; }
[data-testid="stDataFrame"] { color:var(--ink); }
[data-testid="stAlert"] p { color:var(--ink) !important; }
div.stButton > button[kind="primary"] { background:var(--red); border-color:var(--red); border-radius:8px; font-weight:600; }
div.stButton > button { border-radius:8px; }
input, textarea, [data-baseweb="select"] > div { border-radius:8px !important; }
hr { border-color:var(--line); }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="brand">pocket<span>/</span>ledger</div>', unsafe_allow_html=True)
    st.markdown("**YOUR MONEY, IN ORDER**")
    if "_nav_target" in st.session_state:
        st.session_state["_page_nav"] = st.session_state.pop("_nav_target")
    page = st.radio("Navigate", ["Overview", "Add expense", "Expense list"], key="_page_nav", label_visibility="collapsed")
    st.divider()
    st.caption("DSA PROJECT · SORTING")
    st.markdown("Expenses are ordered with **Merge Sort** by amount or date. The active algorithm is shown in the list.")
    st.caption("Your entries stay in this session.")

if page == "Add expense":
    render_expense_form(add_expense)
elif page == "Expense list":
    render_expense_list(st.session_state.expenses)
else:
    render_dashboard(st.session_state.expenses)
