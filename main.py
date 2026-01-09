import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import requests
import time

# API URL
API_URL = "http://localhost:8000"

# Page Config
st.set_page_config(page_title="Financial Dashboard", page_icon="💰", layout="wide")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Quick Add", "Recurring Manager", "Data View"])

# --- PAGE: QUICK ADD ---
if page == "Quick Add":
    st.header("📝 Quick Add")
    
    # --- TRANSACTIONS (Side-by-Side) ---
    st.subheader("New Transaction")
    col_inc, col_exp = st.columns(2)
    
    # LEFT COLUMN: INCOME
    with col_inc:
        st.markdown("### 🟢 Income")
        with st.form("income_form", clear_on_submit=True):
            date_inc = st.date_input("Date", datetime.date.today(), key="date_inc")
            amt_inc = st.number_input("Amount ($)", min_value=0.0, format="%.2f", key="amt_inc")
            cat_inc = st.text_input("Source (e.g., Salary, Bonus)", key="cat_inc")
            note_inc = st.text_area("Notes", height=2, key="note_inc")
            
            sub_inc = st.form_submit_button("Add Income", use_container_width=True)
            
            if sub_inc:
                if amt_inc > 0 and cat_inc:
                    payload = {
                        "date": str(date_inc),
                        "type": "Income",
                        "category": cat_inc,
                        "amount": amt_inc,
                        "notes": note_inc
                    }
                    try:
                        res = requests.post(f"{API_URL}/transactions/", json=payload)
                        if res.status_code == 200:
                            st.toast("✅ Income added successfully!", icon='💰')
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error(f"Error: {res.status_code}")
                    except:
                        st.error("API Error")

    # RIGHT COLUMN: EXPENSE
    with col_exp:
        st.markdown("### 🔴 Expense")
        with st.form("expense_form", clear_on_submit=True):
            date_exp = st.date_input("Date", datetime.date.today(), key="date_exp")
            amt_exp = st.number_input("Amount ($)", min_value=0.0, format="%.2f", key="amt_exp")
            cat_exp = st.text_input("Category (e.g., Food, Rent)", key="cat_exp")
            note_exp = st.text_area("Notes", height=2, key="note_exp")
            
            sub_exp = st.form_submit_button("Add Expense", use_container_width=True)
            
            if sub_exp:
                if amt_exp > 0 and cat_exp:
                    payload = {
                        "date": str(date_exp),
                        "type": "Expense",
                        "category": cat_exp,
                        "amount": amt_exp,
                        "notes": note_exp
                    }
                    try:
                        res = requests.post(f"{API_URL}/transactions/", json=payload)
                        if res.status_code == 200:
                            st.toast("✅ Expense added successfully!", icon='💸')
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error(f"Error: {res.status_code}")
                    except:
                        st.error("API Error")

    st.divider()

    # --- ASSETS (Below) ---
    st.subheader("Update Assets & Liabilities")
    with st.form("asset_form", clear_on_submit=True):
        c1, c2, c3 = st.columns([1, 1, 2])
        with c1:
            a_date = st.date_input("Date", datetime.date.today(), key="asset_date")
        with c2:
            a_type = st.selectbox("Type", ["Cash", "Credit Card Debt", "Investment", "Property"])
        with c3:
            a_name = st.text_input("Name (e.g., Chase Checking, Home)")
            
        a_amount = st.number_input("Current Value ($)", min_value=0.0, format="%.2f", key="asset_amt")
        
        sub_asset = st.form_submit_button("Update Value", use_container_width=True)
        
        if sub_asset:
            if a_amount >= 0 and a_name:
                payload = {
                    "date": str(a_date),
                    "type": a_type,
                    "name": a_name,
                    "amount": a_amount
                }
                try:
                    res = requests.post(f"{API_URL}/assets/", json=payload)
                    if res.status_code == 200:
                        st.success("Asset updated!")
                    else:
                        st.error(f"Error: {res.status_code}")
                except:
                    st.error("API Error")

# --- PAGE: RECURRING MANAGER ---
elif page == "Recurring Manager":
    st.header("🔄 Recurring Manager")
    st.info("Transactions set here will be automatically created on their due dates.")
    
    col_rinc, col_rexp = st.columns(2)
    
    # LEFT COLUMN: RECURRING INCOME
    with col_rinc:
        st.markdown("### 🟢 Recurring Income")
        with st.form("rec_income_form", clear_on_submit=True):
            r_name_inc = st.text_input("Name (e.g., Salary)", key="r_name_inc")
            r_amt_inc = st.number_input("Amount ($)", min_value=0.0, format="%.2f", key="r_amt_inc")
            r_cat_inc = st.text_input("Category", key="r_cat_inc")
            r_freq_inc = st.selectbox("Frequency", ["Monthly", "Weekly", "Daily", "Yearly"], key="r_freq_inc")
            r_start_inc = st.date_input("Start Date", datetime.date.today(), key="r_start_inc")
            
            sub_rinc = st.form_submit_button("Set Recurring Income", use_container_width=True)
            
            if sub_rinc:
                if r_name_inc and r_amt_inc > 0:
                    payload = {
                        "name": r_name_inc, "type": "Income", "category": r_cat_inc,
                        "amount": r_amt_inc, "frequency": r_freq_inc,
                        "start_date": str(r_start_inc), "is_active": True
                    }
                    try:
                        res = requests.post(f"{API_URL}/recurring/", json=payload)
                        if res.status_code == 200:
                            st.toast("✅ Recurring Income set successfully!", icon='💰')
                            time.sleep(2)
                            st.rerun()
                        else: st.error("Error creating item")
                    except requests.exceptions.RequestException: st.error("API Connection Error")
                    except Exception as e: pass

    # RIGHT COLUMN: RECURRING EXPENSE
    with col_rexp:
        st.markdown("### 🔴 Recurring Expense")
        with st.form("rec_expense_form", clear_on_submit=True):
            r_name_exp = st.text_input("Name (e.g., Netflix, Rent)", key="r_name_exp")
            r_amt_exp = st.number_input("Amount ($)", min_value=0.0, format="%.2f", key="r_amt_exp")
            r_cat_exp = st.text_input("Category", key="r_cat_exp")
            r_freq_exp = st.selectbox("Frequency", ["Monthly", "Weekly", "Daily", "Yearly"], key="r_freq_exp")
            r_start_exp = st.date_input("Start Date", datetime.date.today(), key="r_start_exp")
            
            sub_rexp = st.form_submit_button("Set Recurring Expense", use_container_width=True)
            
            if sub_rexp:
                if r_name_exp and r_amt_exp > 0:
                    payload = {
                        "name": r_name_exp, "type": "Expense", "category": r_cat_exp,
                        "amount": r_amt_exp, "frequency": r_freq_exp,
                        "start_date": str(r_start_exp), "is_active": True
                    }
                    try:
                        res = requests.post(f"{API_URL}/recurring/", json=payload)
                        if res.status_code == 200:
                            st.toast("✅ Recurring Expense set successfully!", icon='💸')
                            time.sleep(2)
                            st.rerun()
                        else: st.error("Error creating item")
                    except requests.exceptions.RequestException: st.error("API Connection Error")
                    except Exception as e: pass

    st.divider()
    
    # LIST EXISTING (List + Popup Edit)
    st.subheader("📋 Active Recurring Items")
    
    # Define the Edit Dialog function
    @st.dialog("Edit Recurring Item")
    def edit_recurring_dialog(item):
        with st.form("edit_rec_form"):
            e_name = st.text_input("Name", value=item['name'])
            e_type = st.selectbox("Type", ["Income", "Expense"], index=0 if item['type'] == "Income" else 1)
            e_cat = st.text_input("Category", value=item['category'])
            e_amt = st.number_input("Amount", value=float(item['amount']), min_value=0.0, format="%.2f")
            
            freq_opts = ["Daily", "Weekly", "Monthly", "Yearly"]
            try:
                freq_idx = freq_opts.index(item['frequency'])
            except: freq_idx = 2
            e_freq = st.selectbox("Frequency", freq_opts, index=freq_idx)
            
            # Date handling
            try:
                start_dt = datetime.datetime.strptime(item['start_date'], '%Y-%m-%d').date()
            except: start_dt = datetime.date.today()
            e_start = st.date_input("Start Date", value=start_dt)
            
            e_active = st.checkbox("Active", value=item['is_active'])
            
            if st.form_submit_button("Save Changes"):
                payload = {
                    "name": e_name, "type": e_type, "category": e_cat,
                    "amount": e_amt, "frequency": e_freq,
                    "start_date": str(e_start), "is_active": e_active
                }
                
                success = False
                try:
                    res = requests.put(f"{API_URL}/recurring/{item['id']}", json=payload)
                    if res.status_code == 200:
                        success = True
                    else: st.error(f"Update failed: {res.text}")
                except Exception as e: st.error(f"API Error: {e}")
                
                if success:
                    st.toast("✅ Item updated!", icon="💾")
                    st.rerun()

    # Fetch data
    try:
        res = requests.get(f"{API_URL}/recurring/")
        if res.status_code == 200:
            rec_items = res.json()
            if rec_items:
                # Header
                h1, h2, h3, h4, h5, h6 = st.columns([2, 1, 1, 1, 1, 1])
                h1.markdown("**Name**")
                h2.markdown("**Amount**")
                h3.markdown("**Type**")
                h4.markdown("**Freq**")
                h5.markdown("**Active?**")
                h6.markdown("**Actions**")
                st.divider()
                
                for item in rec_items:
                    c1, c2, c3, c4, c5, c6 = st.columns([2, 1, 1, 1, 1, 1])
                    c1.write(item['name'])
                    c2.write(f"${item['amount']:.2f}")
                    c3.write(item['type'])
                    c4.write(item['frequency'])
                    c5.write("✅" if item['is_active'] else "⏸️")
                    
                    with c6:
                        ec1, ec2 = st.columns(2)
                        if ec1.button("✏️", key=f"edit_{item['id']}", help="Edit"):
                            edit_recurring_dialog(item)
                        
                        if ec2.button("🗑️", key=f"del_{item['id']}", help="Delete"):
                            del_success = False
                            try:
                                d_res = requests.delete(f"{API_URL}/recurring/{item['id']}")
                                if d_res.status_code == 200:
                                    del_success = True
                                else: st.error("Delete failed")
                            except requests.exceptions.RequestException: st.error("API Error")
                            
                            if del_success:
                                st.toast("🗑️ Item deleted")
                                st.rerun()
                    st.divider()

            else:
                st.info("No recurring items found.")
        else:
            st.error("Failed to fetch items.")

    except requests.exceptions.RequestException:
        st.error("Connection Error: Could not reach API")


# --- PAGE: DATA VIEW ---
elif page == "Data View":
    st.header("📄 Data Viewer")
    
    tab1, tab2 = st.tabs(["Transactions", "Asset History"])
    
    with tab1:
        try:
            response = requests.get(f"{API_URL}/transactions/")
            if response.status_code == 200:
                data = response.json()
                if data:
                    df = pd.DataFrame(data)
                    st.dataframe(df.sort_values(by="date", ascending=False), use_container_width=True)
                else:
                    st.info("No transactions found.")
        except:
            st.error("API Error")

    with tab2:
        try:
            response = requests.get(f"{API_URL}/assets/")
            if response.status_code == 200:
                data = response.json()
                if data:
                    df = pd.DataFrame(data)
                    st.dataframe(df.sort_values(by="date", ascending=False), use_container_width=True)
                else:
                    st.info("No asset history found.")
        except:
            st.error("API Error")

# --- PAGE: DASHBOARD ---
elif page == "Dashboard":
    st.header("📊 Financial Overview")
    
    # 1. FETCH DATA
    try:
        t_res = requests.get(f"{API_URL}/transactions/")
        a_res = requests.get(f"{API_URL}/assets/")
        
        transactions = t_res.json() if t_res.status_code == 200 else []
        assets = a_res.json() if a_res.status_code == 200 else []
        
        # 2. PROCESS ASSET DATA (Net Worth Snapshot)
        latest_values = {}
        if assets:
            df_assets = pd.DataFrame(assets)
            df_assets['date'] = pd.to_datetime(df_assets['date'])
            # Sort by date and get last entry for each (type, name)
            df_assets = df_assets.sort_values('date')
            latest_values_df = df_assets.groupby(['type', 'name']).last().reset_index()
            
            # Calculate Totals
            total_cash = latest_values_df[latest_values_df['type'] == 'Cash']['amount'].sum()
            total_debt = latest_values_df[latest_values_df['type'] == 'Credit Card Debt']['amount'].sum()
            total_inv = latest_values_df[latest_values_df['type'] == 'Investment']['amount'].sum()
            total_prop = latest_values_df[latest_values_df['type'] == 'Property']['amount'].sum()
            
            net_worth_assets = (total_cash + total_inv + total_prop) - total_debt
        else:
            total_cash = total_debt = total_inv = total_prop = net_worth_assets = 0.0

        # 3. DISPLAY TRANSACTION-BASED NET WORTH GRAPH (Cash Flow)
        if transactions:
            df = pd.DataFrame(transactions)
            df['date'] = pd.to_datetime(df['date'])
            
            # Create a signed amount column: Income is positive, Expense is negative
            df['signed_amount'] = df.apply(lambda x: x['amount'] if x['type'] == 'Income' else -x['amount'], axis=1)
            
            # Group by date for the graph
            daily_df = df.groupby('date')['signed_amount'].sum().reset_index()
            daily_df = daily_df.sort_values('date')
            daily_df['running_balance'] = daily_df['signed_amount'].cumsum()
            
            current_run_bal = daily_df['running_balance'].iloc[-1]
            
            st.subheader("📈 Net Worth (Cumulative Cash Flow)")
            fig_net_worth = px.line(daily_df, x='date', y='running_balance', markers=True, 
                                    labels={'running_balance': 'Cumulative Balance ($)', 'date': 'Date'})
            fig_net_worth.update_traces(line_color='#2ca02c') # Green line
            fig_net_worth.update_xaxes(tickformat="%Y-%m-%d", dtick="D1")
            
            st.plotly_chart(fig_net_worth, use_container_width=True)
            
        else:
            st.info("Add transactions to see the Net Worth Trend Graph.")

        st.divider()

        # 4. DISPLAY ASSET BREAKDOWN (Snapshots)
        st.subheader("💰 Asset & Liability Breakdown")
        st.caption("Based on latest updated values.")
        
        # Display Total Net Worth from Assets
        st.metric(label="Total Net Worth (Assets - Debts)", value=f"${net_worth_assets:,.2f}")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💵 Cash", f"${total_cash:,.2f}")
        col2.metric("💳 Debt", f"${total_debt:,.2f}", delta_color="inverse")
        col3.metric("📈 Investments", f"${total_inv:,.2f}")
        col4.metric("🏠 Property", f"${total_prop:,.2f}")
        
        st.divider()

        # 5. PERIOD ANALYSIS (Bottom Section)
        if transactions:
            st.subheader("📅 Monthly Income & Expenses Analysis")
            
            c1, c2 = st.columns(2)
            with c1:
                start_date = st.date_input("Start Date", df['date'].min())
            with c2:
                end_date = st.date_input("End Date", datetime.date.today())

            mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
            filtered_df = df.loc[mask]

            if not filtered_df.empty:
                # KPIS
                inc = filtered_df[filtered_df['type'] == 'Income']['amount'].sum()
                exp = filtered_df[filtered_df['type'] == 'Expense']['amount'].sum()
                sav = inc - exp
                
                k1, k2, k3 = st.columns(3)
                k1.metric("Income", f"${inc:,.2f}")
                k2.metric("Expenses", f"${exp:,.2f}", delta_color="inverse")
                k3.metric("Savings", f"${sav:,.2f}")
                
                # Charts
                ch1, ch2 = st.columns(2)
                with ch1:
                    exp_df = filtered_df[filtered_df['type'] == 'Expense']
                    if not exp_df.empty:
                        fig = px.pie(exp_df, values='amount', names='category', hole=0.4, title="Expenses by Category")
                        st.plotly_chart(fig, use_container_width=True)
                with ch2:
                    # Daily Trend
                    trend = filtered_df.groupby([filtered_df['date'].dt.date, 'type'])['amount'].sum().reset_index()
                    if not trend.empty:
                        fig = px.bar(trend, x='date', y='amount', color='type', title="Daily Trend",
                                     color_discrete_map={'Income': 'green', 'Expense': 'red'})
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No transactions in selected range.")

    except Exception as e:
        st.error(f"Error loading dashboard: {e}")