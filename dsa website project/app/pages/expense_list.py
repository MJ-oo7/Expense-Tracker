import streamlit as st

from service.sorting import merge_sort
from utils.formatting import display_date, money


def render_expense_list(expenses):
    st.markdown('<div class="eyebrow">YOUR LEDGER</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Expense list</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">Every transaction, ready to be explored.</div>', unsafe_allow_html=True)
    st.write("")
    if not expenses:
        st.info("Your ledger is empty. Add your first expense to see it here.")
        return
    c1, c2 = st.columns([1, 2])
    with c1:
        sort_by = st.selectbox("Sort by", ["Date", "Amount (highest first)", "Amount (lowest first)", "Name"])
    if sort_by == "Date":
        ordered = merge_sort(expenses, key=lambda item: item["date"], descending=True)
    elif sort_by == "Amount (highest first)":
        ordered = merge_sort(expenses, key=lambda item: item["amount"], descending=True)
    elif sort_by == "Amount (lowest first)":
        ordered = merge_sort(expenses, key=lambda item: item["amount"])
    else:
        ordered = merge_sort(expenses, key=lambda item: item["name"].lower())
    st.caption(f"Sorted with Merge Sort · {len(ordered)} transaction{'s' if len(ordered) != 1 else ''} · O(n log n)")
    st.dataframe([{"Date": display_date(e["date"]), "Name": e["name"], "Category": e["category"], "Amount": money(e["amount"]), "Note": e["note"]} for e in ordered], use_container_width=True, hide_index=True)
