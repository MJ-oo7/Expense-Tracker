from datetime import date

import streamlit as st

from service.sorting import merge_sort
from utils.formatting import display_date, money


def render_dashboard(expenses):
    st.markdown('<div class="eyebrow">A CLEARER VIEW OF YOUR SPENDING</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Expense Tracker</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">A simple ledger for the little things that add up.</div>', unsafe_allow_html=True)
    st.write("")
    total = sum(e["amount"] for e in expenses)
    highest = merge_sort(expenses, key=lambda e: e["amount"], descending=True)[0] if expenses else None
    today = date.today()
    this_month = [e for e in expenses if e["date"].year == today.year and e["date"].month == today.month]
    a, b, c = st.columns(3)
    a.metric("Total expenses", money(total))
    b.metric("Transactions", len(expenses))
    c.metric("This month", money(sum(e["amount"] for e in this_month)))
    st.write("")
    left, right = st.columns([1.15, .85], gap="large")
    with left:
        st.markdown('<div class="eyebrow">RECENT ACTIVITY</div>', unsafe_allow_html=True)
        st.subheader("Latest expenses")
        if expenses:
            recent = merge_sort(expenses, key=lambda e: e["date"], descending=True)[:5]
            st.dataframe([{"Date": display_date(e["date"]), "Expense": e["name"], "Category": e["category"], "Amount": money(e["amount"])} for e in recent], use_container_width=True, hide_index=True)
        else:
            st.markdown('<div class="panel"><span class="subtle">No expenses yet. Add your first one to start your ledger.</span></div>', unsafe_allow_html=True)
            if st.button("＋  Add your first expense", type="primary"):
                st.session_state["_nav_target"] = "Add expense"
                st.rerun()
    with right:
        st.markdown('<div class="eyebrow">BIGGEST SPEND</div>', unsafe_allow_html=True)
        st.subheader("Your highest expense")
        if highest:
            st.markdown(f'<div class="panel"><div class="metric-label">{highest["category"]} · {display_date(highest["date"])}</div><div class="metric-value">{money(highest["amount"])}</div><div class="small-note">{highest["name"]}</div></div>', unsafe_allow_html=True)
            by_category = {}
            for expense in expenses:
                by_category[expense["category"]] = by_category.get(expense["category"], 0) + expense["amount"]
            st.write("")
            st.markdown('<div class="eyebrow">SPENDING BY CATEGORY</div>', unsafe_allow_html=True)
            st.bar_chart(by_category, color="#23745c", height=220)
        else:
            st.markdown('<div class="panel"><span class="subtle">Your biggest spend will show here once you add an expense.</span></div>', unsafe_allow_html=True)
