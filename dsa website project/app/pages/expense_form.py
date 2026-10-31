import streamlit as st

from config.settings import CATEGORIES


def render_expense_form(add_expense):
    st.markdown('<div class="eyebrow">NEW TRANSACTION</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Add an expense</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">Capture the details now. You can sort and review everything later.</div>', unsafe_allow_html=True)
    st.write("")
    left, form_col, right = st.columns([1, 1.35, 1])
    with form_col:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        with st.form("expense_form", clear_on_submit=True):
            name = st.text_input("Name of expense", placeholder="e.g. Lunch with friends")
            amount = st.number_input("Amount (₱)", min_value=0.01, value=100.00, step=50.00, format="%.2f")
            category = st.selectbox("Category", CATEGORIES)
            spent_on = st.date_input("Date")
            note = st.text_input("Note (optional)", placeholder="Add a little context")
            submitted = st.form_submit_button("Add expense  →", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if submitted:
            if not name.strip():
                st.error("Give this expense a name before saving.")
            else:
                st.session_state.expenses = add_expense(st.session_state.expenses, name, amount, category, spent_on, note)
                st.success(f"{name.strip()} added to your ledger.")
                st.rerun()
