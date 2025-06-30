import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import hashlib
import subprocess
import sys

st.set_page_config(page_title="Atlas Dashboard", layout="wide")

# Database setup
def get_connection():
    return sqlite3.connect('atlas_dashboard.db', check_same_thread=False)

def create_tables():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS document_logs (
        SN INTEGER PRIMARY KEY AUTOINCREMENT,
        "DOCUMENT TYPE" TEXT,
        "VENDOR" TEXT,
        "DOCUMENT STATUS" TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS shop_drawing_logs (
        SN INTEGER PRIMARY KEY AUTOINCREMENT,
        "System" TEXT,
        "Sub System" TEXT,
        "Drawing Submission Status" TEXT,
        "292" TEXT
    )''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup(username, password, role):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hash_password(password), role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username=? AND password=?", (username, hash_password(password)))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

def run_data_cleaning_script():
    subprocess.run([sys.executable, "data_cleaning_script.py"], check=True)

create_tables()

# --- Shared Styles ---
st.markdown("""
    <style>
        .main, .stApp {
            background-color: #f8fbff;
        }
        .stTabs [data-baseweb="tab-list"] {
            background-color: #1976d2;
            padding: 0.5rem 2rem;
            border-radius: 1.5rem;
            margin-bottom: 2rem;
            gap: 2rem;
            display: flex;
            justify-content: center;
        }
        .stTabs [data-baseweb="tab"] {
            color: white;
            font-size: 1.1rem;
            font-weight: 600;
            padding: 0.7rem 2.5rem;
            border-radius: 1.5rem;
            margin: 0 0.5rem;
            transition: background 0.3s, color 0.3s;
        }
        .stTabs [aria-selected="true"] {
            background: #fff !important;
            color: #1976d2 !important;
            box-shadow: 0 2px 8px rgba(25, 118, 210, 0.08);
        }
        .stTabs [aria-selected="false"] {
            background: #1976d2 !important;
            color: #fff !important;
        }
        .stButton>button {
            background-color: #1976d2;
            color: white;
            border-radius: 0.5rem;
            font-weight: 600;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #1976d2;
            font-family: 'Segoe UI', 'Arial', sans-serif;
        }
        .custom-title {
            font-size:2.5rem;
            font-weight:800;
            letter-spacing:2px;
            color:#111;
            font-family: 'Segoe UI', 'Arial', sans-serif;
            margin-bottom:0.5rem;
        }
        .custom-section {
            font-size:1.5rem;
            font-weight:700;
            letter-spacing:1px;
            color:#111;
            font-family: 'Segoe UI', 'Arial', sans-serif;
            margin-top:2.5rem;
            margin-bottom:1.5rem;
            border-left: 6px solid #1976d2;
            padding-left: 18px;
            background: linear-gradient(90deg, #f8fbff 80%, #e3f0fc 100%);
            border-radius: 0.5rem;
            box-shadow: 0 2px 8px rgba(25, 118, 210, 0.03);
        }
        .stDataFrame, .stTable {
            background: #fff;
            border-radius: 1rem;
            box-shadow: 0 2px 8px rgba(25, 118, 210, 0.05);
        }
        .atlas-title {
            font-size:2.5rem;
            font-weight:800;
            letter-spacing:2px;
            color:#111;
            font-family: 'Segoe UI', 'Arial', sans-serif;
            margin-bottom:0.5rem;
        }
        .center-form {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .center-form .stTextInput>div>div>input,
        .center-form .stTextInput>div>div>div>input,
        .center-form .stPasswordInput>div>div>input,
        .center-form .stPasswordInput>div>div>div>input {
            width: 260px !important;
            min-width: 180px !important;
            max-width: 320px !important;
        }
        .center-form .stButton>button {
            width: 120px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Navigation State ---
if "page" not in st.session_state:
    st.session_state.page = "home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None

def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.page = "home"

# --- Home Page ---
if st.session_state.page == "home":
    col1, col2 = st.columns([3, 4])
    with col1:
        st.markdown(
            "<div class='atlas-title' style='margin-top:2.5rem; display: flex; align-items: center;'>Welcome to Atlas Dashboard</div>",
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            "<div style='display: flex; align-items: center; height: 100%; justify-content: flex-start; margin-top: 2.5rem;'>",
            unsafe_allow_html=True
        )
        st.image("atlas_logo.jpg", width=70)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style='font-size:1.2rem;margin-bottom:2rem;'>
            Please <b>Login</b> or <b>Signup</b> to access the dashboards.<br>
            <br>
            <ul>
                <li><b>Editors</b> can create, update, and delete logs.</li>
                <li><b>Viewers</b> can only view logs.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True
    )

    tab = st.tabs(["Login", "Signup"])
    with tab[0]:
        st.markdown('<div class="center-form">', unsafe_allow_html=True)
        st.subheader("Login")
        user = st.text_input("Username", key="login_user")
        pwd = st.text_input("Password", type="password", key="login_pwd")
        if st.button("Login"):
            role = login(user, pwd)
            if role:
                st.session_state.logged_in = True
                st.session_state.role = role
                st.session_state.username = user
                st.session_state.page = "dashboard"
                st.success(f"Logged in as {user} ({role})")
                st.rerun()
            else:
                st.error("Invalid credentials.")
        st.markdown('</div>', unsafe_allow_html=True)
    with tab[1]:
        st.markdown('<div class="center-form">', unsafe_allow_html=True)
        st.subheader("Signup")
        new_user = st.text_input("New Username", key="signup_user")
        new_pass = st.text_input("New Password", type="password", key="signup_pwd")
        role = st.selectbox("Role", ["editor", "viewer"], key="signup_role")
        if st.button("Signup"):
            if signup(new_user, new_pass, role):
                st.success("Signup successful! Please login.")
            else:
                st.error("Username already exists.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- Dashboard Page ---
elif st.session_state.page == "dashboard" and st.session_state.logged_in:
    st.sidebar.markdown(f"**Logged in as:** {st.session_state.username} ({st.session_state.role})")
    if st.sidebar.button("Logout"):
        logout()
        st.rerun()

    # --- SYNC BUTTON ---
    if st.sidebar.button("Sync Data from Excel"):
        run_data_cleaning_script()
        st.success("Data synced from Excel files!")
        st.rerun()

    sidebar_choice = st.sidebar.radio(
        "Select Dashboard",
        ("Document Dashboard", "Shop Drawing Dashboard")
    )

    # --- Document Dashboard ---
    if sidebar_choice == "Document Dashboard":
        logo_col, title_col = st.columns([0.13, 0.87])
        with logo_col:
            st.image("atlas_logo.jpg", width=70)
        with title_col:
            st.markdown(
                "<div class='custom-title'>Atlas Document Dashboard</div>",
                unsafe_allow_html=True
            )
        try:
            df1 = pd.read_csv('df1_cleaned.csv')
        except FileNotFoundError:
            st.error("Error: df1_cleaned.csv not found. Make sure the file is in the correct directory.")
            st.stop() 

        tabs = st.tabs([
            "   📊  Document Status Overview   ",
            "   📋  Document Log Viewer   ",
            "   📝  Document Edit Log   "
        ])

        # --- Document Status Overview ---
        with tabs[0]:
            st.markdown("<div class='custom-section'>Document Status Overview</div>", unsafe_allow_html=True)
            col1, col2 = st.columns([1,3])
            with col1:
                if 'DOCUMENT STATUS' in df1.columns:
                    status_col = df1['DOCUMENT STATUS'].astype(str).str.strip().str.upper()
                    pending_count = (status_col == 'PENDING').sum()
                    submitted_count = (status_col == 'SUBMITTED').sum()
                    status_df = pd.DataFrame({
                        'Status': ['Pending', 'Submitted'],
                        'Count': [pending_count, submitted_count]
                    })
                    fig1 = px.pie(
                        status_df,
                        names='Status',
                        values='Count',
                        hole=0.45,
                        width=380,
                        height=430,
                        color='Status',
                        color_discrete_map={'Pending': '#ff9800', 'Submitted': '#1976d2'}
                    )
                    fig1.update_traces(textinfo='percent+label', showlegend=False)
                    fig1.update_layout(title_text="Pending vs Submitted", title_font_color="#1976d2")
                    st.plotly_chart(fig1, use_container_width=False)
                else:
                    st.warning("No 'DOCUMENT STATUS' column found for visualization.")
            with col2:
                st.markdown(f"""
                <div style='
                    background: linear-gradient(90deg, #1976d2 0%, #90caf9 100%);
                    border-radius: 1rem;
                    padding: 2rem 2.5rem;
                    margin-top: 2.5rem;
                    margin-bottom: 2rem;
                    color: white;
                    font-size: 1.3rem;
                    font-weight: 500;
                    box-shadow: 0 2px 8px rgba(25, 118, 210, 0.08);
                    display: flex;
                    flex-direction: row;
                    gap: 3rem;
                    justify-content: center;
                '>
                    <div style='min-width:150px; text-align:center;'>
                        <span style='font-size:2.5rem;font-weight:700;'>{len(df1)}</span><br>Total Documents
                    </div>
                    <div style='min-width:150px; text-align:center;'>
                        <span style='font-size:2.5rem;font-weight:700;'>{submitted_count if 'DOCUMENT STATUS' in df1.columns else '-'}</span><br>Submitted
                    </div>
                    <div style='min-width:150px; text-align:center;'>
                        <span style='font-size:2.5rem;font-weight:700;'>{pending_count if 'DOCUMENT STATUS' in df1.columns else '-'}</span><br>Pending
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Vendor vs Document Type Stacked Bar Chart
            st.markdown("<div class='custom-section'>Vendor vs Document Type Stacked Bar Chart</div>", unsafe_allow_html=True)
            if 'DOCUMENT TYPE' in df1.columns and 'VENDOR' in df1.columns:
                stacked_df = (
                    df1.groupby(['VENDOR', 'DOCUMENT TYPE'])
                    .size()
                    .reset_index(name='Count')
                )
                if not stacked_df.empty:
                    fig = px.bar(
                        stacked_df,
                        x='VENDOR',
                        y='Count',
                        color='DOCUMENT TYPE',
                        barmode='stack',
                        title="Stacked Bar: Document Type Distribution per Vendor"
                    )
                    fig.update_layout(
                        title_font_color="#1976d2",
                        legend_title_text='Document Type',
                        xaxis_title="Vendor",
                        yaxis_title="Document Count"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for Vendor vs Document Type Stacked Bar Chart.")
            else:
                st.info("Required columns ('DOCUMENT TYPE' and 'VENDOR') not found for this chart.")

            # Submittal Type Distribution (from CATEGORIES)
            st.markdown("<div class='custom-section'>Submittal Type Distribution</div>", unsafe_allow_html=True)
            if 'CATEGORIES' in df1.columns:
                cat_col = df1['CATEGORIES'].astype(str).str.strip().str.upper()
                submittal_df = cat_col.value_counts().reset_index()
                submittal_df.columns = ['Submittal Type', 'Count']
                fig2 = px.bar(
                    submittal_df,
                    x='Submittal Type',
                    y='Count',
                    color='Submittal Type',
                    title="Project vs Closeout Submittals",
                    width=500,
                    height=320,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig2.update_layout(legend_title_text='Submittal Type', title_font_color="#1976d2")
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No 'CATEGORIES' column found for submittal type distribution.")

            # --- Submission Code Distribution ---
            st.markdown("<div class='custom-section'>Submission Code Distribution</div>", unsafe_allow_html=True)
            if 'STATUS_C' in df1.columns:
                code_col = df1['STATUS_C'].astype(str).str.strip().str.upper()
                code_categories = ['CODE 1', 'CODE 2', 'CODE 3', 'AR (ATJV)', 'UR (DAR)', 'UR (ATJV)']
                code_counts = [(code_col == code).sum() for code in code_categories]
                not_submitted_count = code_col.isna().sum() + (code_col == '').sum() + ((~code_col.isin(code_categories)) & (code_col != '') & (~code_col.isna())).sum()
                all_counts = code_counts + [not_submitted_count]
                all_labels = code_categories + ['NOT SUBMITTED']
                # Bar chart
                code_df = pd.DataFrame({'Code': all_labels, 'Count': all_counts})
                fig3 = px.bar(
                    code_df,
                    x='Code',
                    y='Count',
                    color='Code',
                    text='Count',
                    color_discrete_sequence=['#1565c0', '#1976d2', '#2196f3', '#64b5f6', '#90caf9', '#42a5f5', '#b3e5fc'],
                    title=""
                )
                fig3.update_layout(
                    xaxis_title="Code",
                    yaxis_title="Number of Logs",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#1976d2",
                    legend_title_text='Submission Code',
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                fig3.update_traces(textposition='outside')
                st.plotly_chart(fig3, use_container_width=True)
                # Blue pane with code counts
                st.markdown(
                    "<div style='background: linear-gradient(90deg, #1976d2 0%, #90caf9 100%);"
                    "border-radius: 1rem; padding: 2rem 2.5rem; margin: 2rem 0 2rem 0; color: white; "
                    "font-size: 1.3rem; font-weight: 500; box-shadow: 0 2px 8px rgba(25, 118, 210, 0.08);"
                    "display: flex; flex-direction: row; gap: 3rem; justify-content: center;'>"
                    + "".join([
                        f"<div style='min-width:150px; text-align:center;'>"
                        f"<span style='font-size:2.5rem;font-weight:700;'>{count}</span><br>{label}</div>"
                        for count, label in zip(all_counts, all_labels)
                    ])
                    + "</div>",
                    unsafe_allow_html=True
                )
            else:
                st.info("No 'STATUS_C' column found.")

        # --- Document Log Viewer ---
        with tabs[1]:
            st.markdown("<div class='custom-section'>Document Log Viewer</div>", unsafe_allow_html=True)
            document_types = ['All']
            if 'DOCUMENT TYPE' in df1.columns:
                document_types += sorted([str(d) for d in df1['DOCUMENT TYPE'].unique() if str(d).lower() != 'nan'])
            vendor_names = ['All']
            if 'VENDOR' in df1.columns:
                vendor_names += sorted([str(v) for v in df1['VENDOR'].unique() if str(v).lower() != 'nan'])
            selected_doc_type = st.selectbox('Filter by Document Type:', document_types, key="view_doc_type")
            selected_vendor = st.selectbox('Filter by Vendor Name:', vendor_names, key="view_vendor")
            filtered_df1 = df1.copy()
            if selected_doc_type != 'All':
                filtered_df1 = filtered_df1[filtered_df1['DOCUMENT TYPE'] == selected_doc_type]
            if selected_vendor != 'All':
                filtered_df1 = filtered_df1[filtered_df1['VENDOR'] == selected_vendor]
            st.dataframe(filtered_df1, use_container_width=True, height=400)

        # --- Document Edit Log ---
        with tabs[2]:
            st.markdown("<div class='custom-section'>Document Edit Log</div>", unsafe_allow_html=True)
            if st.session_state.role == "editor":
                edit_df = df1.copy()
                edited = st.data_editor(edit_df, use_container_width=True, height=400, num_rows="dynamic")
                st.info("You can edit the table above. (Saving to CSV not implemented in this example.)")
            else:
                st.warning("Only editors can access the edit log.")

    # --- Shop Drawing Dashboard ---
    elif sidebar_choice == "Shop Drawing Dashboard":
        logo_col, title_col = st.columns([0.13, 0.87])
        with logo_col:
            st.image("atlas_logo.jpg", width=70)
        with title_col:
            st.markdown(
                "<div class='custom-title'>Shop Drawing Dashboard</div>",
                unsafe_allow_html=True
            )
        try:
            df = pd.read_csv('df2_cleaned.csv')
        except FileNotFoundError:
            st.error("Error: df2_cleaned.csv not found. Make sure the file is in the correct directory.")
            st.stop()

        tabs = st.tabs([
            "   📊  Drawing Status Overview   ",
            "   📋  View Drawing Logs   ",
            "   📝  Shop Drawing Edit Log   "
        ])

        # --- Drawing Status Overview ---
        with tabs[0]:
            st.markdown("<div class='custom-section'>Drawing Status Overview</div>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 3])
            with col1:
                if 'Drawing Submission Status' in df.columns:
                    status_col = df['Drawing Submission Status'].astype(str).str.strip().str.upper()
                    pending_count = (status_col == 'PENDING').sum()
                    submitted_count = (status_col == 'SUBMITTED').sum()
                    status_df = pd.DataFrame({
                        'Status': ['Pending', 'Submitted'],
                        'Count': [pending_count, submitted_count]
                    })
                    fig1 = px.pie(
                        status_df,
                        names='Status',
                        values='Count',
                        hole=0.45,
                        width=380,
                        height=430,
                        color='Status',
                        color_discrete_map={'Pending': '#ff9800', 'Submitted': '#1976d2'}
                    )
                    fig1.update_traces(textinfo='percent+label', showlegend=False)
                    fig1.update_layout(title_text="Pending vs Submitted", title_font_color="#1976d2")
                    st.plotly_chart(fig1, use_container_width=False)
                else:
                    st.warning("No 'Drawing Submission Status' column found for visualization.")
            with col2:
                st.markdown(f"""
                <div style='
                    background: linear-gradient(90deg, #1976d2 0%, #90caf9 100%);
                    border-radius: 1rem;
                    padding: 2rem 2.5rem;
                    margin-top: 2.5rem;
                    margin-bottom: 2rem;
                    color: white;
                    font-size: 1.3rem;
                    font-weight: 500;
                    box-shadow: 0 2px 8px rgba(25, 118, 210, 0.08);
                    display: flex;
                    flex-direction: row;
                    gap: 3rem;
                    justify-content: center;
                '>
                    <div style='min-width:150px; text-align:center;'>
                        <span style='font-size:2.5rem;font-weight:700;'>{len(df)}</span><br>Total Drawings
                    </div>
                    <div style='min-width:150px; text-align:center;'>
                        <span style='font-size:2.5rem;font-weight:700;'>{submitted_count if 'Drawing Submission Status' in df.columns else '-'}</span><br>Submitted
                    </div>
                    <div style='min-width:150px; text-align:center;'>
                        <span style='font-size:2.5rem;font-weight:700;'>{pending_count if 'Drawing Submission Status' in df.columns else '-'}</span><br>Pending
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Subsystem Counts per System
            st.markdown("<div class='custom-section'>Subsystem Counts per System</div>", unsafe_allow_html=True)
            if 'System' in df.columns and 'Sub System' in df.columns:
                subsys_counts = (
                    df.groupby(['System', 'Sub System'])
                    .size()
                    .reset_index(name='Count')
                )
                fig = px.bar(
                    subsys_counts,
                    x='Sub System',
                    y='Count',
                    color='System',
                    text='Count',
                    barmode='group',
                    title="Subsystem Counts per System"
                )
                fig.update_layout(
                    xaxis_title="Sub-System",
                    yaxis_title="Count",
                    title_font_color="#1976d2",
                    plot_bgcolor="#f8fbff",
                    paper_bgcolor="#f8fbff",
                    xaxis_tickangle=-45
                )
                fig.update_traces(textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Required columns 'System' and 'Sub System' not found in data.")

            # --- Drawing Codes Distribution ---
            st.markdown("<div class='custom-section'>Drawing Codes Distribution</div>", unsafe_allow_html=True)
            if '28' in df.columns:
                code_col = df['28'].astype(str).str.strip().str.upper()
                code_categories = ['CODE 1', 'CODE 2', 'CODE 3', 'AR (ATJV)', 'UR (DAR)', 'UR (ATJV)']
                code_counts = [(code_col == code).sum() for code in code_categories]
                not_submitted_count = code_col.isna().sum() + (code_col == '').sum() + ((~code_col.isin(code_categories)) & (code_col != '') & (~code_col.isna())).sum()
                all_counts = code_counts + [not_submitted_count]
                all_labels = code_categories + ['NOT SUBMITTED']
                # Bar chart
                code_df = pd.DataFrame({'Code': all_labels, 'Count': all_counts})
                fig2 = px.bar(
                    code_df,
                    x='Code',
                    y='Count',
                    color='Code',
                    text='Count',
                    color_discrete_sequence=['#1565c0', '#1976d2', '#2196f3', '#64b5f6', '#90caf9', '#42a5f5', '#b3e5fc'],
                    title=""
                )
                fig2.update_layout(
                    xaxis_title="Code",
                    yaxis_title="Number of Logs",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#1976d2",
                    legend_title_text='Drawing Code',
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                fig2.update_traces(textposition='outside')
                st.plotly_chart(fig2, use_container_width=True)
                # Blue pane with code counts
                st.markdown(
                    "<div style='background: linear-gradient(90deg, #1976d2 0%, #90caf9 100%);"
                    "border-radius: 1rem; padding: 2rem 2.5rem; margin: 2rem 0 2rem 0; color: white; "
                    "font-size: 1.3rem; font-weight: 500; box-shadow: 0 2px 8px rgba(25, 118, 210, 0.08);"
                    "display: flex; flex-direction: row; gap: 3rem; justify-content: center;'>"
                    + "".join([
                        f"<div style='min-width:150px; text-align:center;'>"
                        f"<span style='font-size:2.5rem;font-weight:700;'>{count}</span><br>{label}</div>"
                        for count, label in zip(all_counts, all_labels)
                    ])
                    + "</div>",
                    unsafe_allow_html=True
                )
            else:
                st.info("No '292' column found.")

        # --- View Drawing Logs ---
        with tabs[1]:
            st.markdown("<div class='custom-section'>View Drawing Logs</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                system_options = ["All"] + sorted(df["System"].dropna().unique().tolist()) if "System" in df.columns else []
                selected_system = st.selectbox("Filter by System", system_options)
            with col2:
                if selected_system != "All" and "Sub System" in df.columns:
                    subsystem_options = ["All"] + sorted(df[df["System"] == selected_system]["Sub System"].dropna().unique().tolist())
                elif "Sub System" in df.columns:
                    subsystem_options = ["All"] + sorted(df["Sub System"].dropna().unique().tolist())
                else:
                    subsystem_options = []
                selected_subsystem = st.selectbox("Filter by Sub-System", subsystem_options)

            filtered_df = df.copy()
            if selected_system != "All" and "System" in filtered_df.columns:
                filtered_df = filtered_df[filtered_df["System"] == selected_system]
            if selected_subsystem != "All" and "Sub System" in filtered_df.columns:
                filtered_df = filtered_df[filtered_df["Sub System"] == selected_subsystem]
            st.dataframe(filtered_df, use_container_width=True, height=400)

        # --- Shop Drawing Edit Log ---
        with tabs[2]:
            st.markdown("<div class='custom-section'>Shop Drawing Edit Log</div>", unsafe_allow_html=True)
            if st.session_state.role == "editor":
                edit_df = df.copy()
                edited = st.data_editor(edit_df, use_container_width=True, height=400, num_rows="dynamic")
                st.info("You can edit the table above. (Saving to CSV not implemented in this example.)")
            else:
                st.warning("Only editors can access the edit log.")

# --- Footer ---
st.markdown("<footer style='text-align: center; margin-top: 2rem; padding: 1rem; background-color: #f1f1f1; border-radius: 0.5rem;'>© 2023 Atlas Dashboard</footer>", unsafe_allow_html=True)