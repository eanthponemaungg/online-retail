import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Online Retail Mini Dashboard",
    layout="centered",
    page_icon="📊"
)


st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #FFFFFF; color: #000000; }
[data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 2px solid #000000 !important; }
h1, h2, h3, h4, label, p { color: #000000 !important; font-family: 'Inter', sans-serif; text-transform: uppercase; letter-spacing: 0.05em; }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if "role" not in st.session_state:
    st.session_state.role = None

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 5, 1])
    with col2:
        st.title("ONLINE RETAIL Dataset System")
        st.header("LOGIN")

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Login")

            if login_btn:
                if username == "AdminRIG" and password == "AdminRIG123*@":
                    st.session_state.logged_in = True
                    st.session_state.page = "manage"
                    st.session_state.role = "AdminRIG"
                    st.success("✅ Admin Login successful")
                    st.experimental_rerun()
                elif username == "UserRIG" and password == "UserRIG456*@":
                    st.session_state.logged_in = True
                    st.session_state.page = "analysis"
                    st.session_state.role = "UserRIG"
                    st.success("✅ User Login successful")
                    st.experimental_rerun()
                else:
                    st.error("❌ Invalid username or password! Contact your supervisor.")
    st.stop()

with st.sidebar:
    st.title("WELCOME BACK 👋🏼")
    st.info("You've logged into your account!")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.session_state.role = None
        st.experimental_rerun()

@st.cache_data
def load_data():
    url = "https://github.com/eanthponemaungg/online-retail/blob/main/online_retail_mini.xlsx"  # <- replace with your raw GitHub URL
    df = pd.read_excel(url, engine="openpyxl")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["TotalSales"] = df["Quantity"] * df["Price"]
    return df

df = load_data()

if st.session_state.page == "manage":
    st.title("Data Management Panel")
    action = st.selectbox("Choose Action", ["Add Record", "Update Record", "Delete Record"])

    if action == "Add Record":
        with st.form("add_form"):
            invoice = st.text_input("Invoice No")
            country = st.text_input("Country")
            quantity = st.number_input("Quantity", min_value=1)
            price = st.number_input("Price", min_value=0.0)
            date = st.date_input("Invoice Date")
            submit_add = st.form_submit_button("Add Record")
            if submit_add:
                new_row = {
                    "Invoice": invoice, "Country": country,
                    "Quantity": quantity, "Price": price,
                    "InvoiceDate": date, "TotalSales": quantity * price
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                st.success("✅ Record Added Successfully")

    elif action == "Update Record":
        invoice_list = df["Invoice"].astype(str).unique()
        selected_invoice = st.selectbox("Select Invoice", invoice_list)
        record = df[df["Invoice"].astype(str) == selected_invoice].iloc[0]
        with st.form("update_form"):
            quantity = st.number_input("Quantity", value=int(record["Quantity"]))
            price = st.number_input("Price", value=float(record["Price"]))
            submit_update = st.form_submit_button("Update Record")
            if submit_update:
                df.loc[df["Invoice"].astype(str) == selected_invoice, ["Quantity", "Price", "TotalSales"]] = [
                    quantity, price, quantity * price
                ]
                st.success("✅ Record Updated Successfully")

    elif action == "Delete Record":
        invoice_list = df["Invoice"].astype(str).unique()
        selected_invoice = st.selectbox("Select Invoice to Delete", invoice_list)
        if st.button("Delete Record"):
            df = df[df["Invoice"].astype(str) != selected_invoice]
            st.warning("🗑️ Record Deleted")

    st.divider()
    if st.button("➡️ Go to Analysis Dashboard"):
        st.session_state.page = "analysis"
        st.experimental_rerun()

if st.session_state.page != "analysis":
    st.stop()

with st.sidebar:
    st.title("Online Retail Dashboard")
    st.subheader("Settings")
    date_range = st.slider(
        "Select Date Range",
        min_value=df["InvoiceDate"].min().date(),
        max_value=df["InvoiceDate"].max().date(),
        value=(df["InvoiceDate"].min().date(), df["InvoiceDate"].max().date())
    )
    country = st.multiselect(
        "Select Country",
        df["Country"].dropna().unique(),
        default=df["Country"].dropna().unique()
    )

filtered_df = df[
    (df["InvoiceDate"].dt.date >= date_range[0]) &
    (df["InvoiceDate"].dt.date <= date_range[1]) &
    (df["Country"].isin(country))
]

st.title("Online Retail Analysis Details")

st.header("RECORD DETAILS")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Total Sales by Country")
    sales_country = filtered_df.groupby("Country")["TotalSales"].sum().reset_index()
    st.bar_chart(sales_country, x="Country", y="TotalSales")

with col2:
    st.subheader("Total Quantity Sold by Country")
    qty_country = filtered_df.groupby("Country")["Quantity"].sum().reset_index()
    st.bar_chart(qty_country, x="Country", y="Quantity")

st.header("SALES RELATIONSHIPS")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Price vs Quantity")
    st.scatter_chart(filtered_df, x="Price", y="Quantity")

with col2:
    st.subheader("Quantity vs Total Sales")
    st.scatter_chart(filtered_df, x="Quantity", y="TotalSales")

st.header("TIME-BASED ANALYSIS")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Daily Total Sales")
    daily_sales = filtered_df.groupby(filtered_df["InvoiceDate"].dt.date)["TotalSales"].sum().reset_index().set_index("InvoiceDate")
    st.line_chart(daily_sales)

with col2:
    st.subheader("Daily Total Quantity")
    daily_qty = filtered_df.groupby(filtered_df["InvoiceDate"].dt.date)["Quantity"].sum().reset_index().set_index("InvoiceDate")
    st.line_chart(daily_qty)

st.divider()
if st.session_state.role == "AdminRIG":
    if st.button("⬅️ Go Back to Data Management Panel"):
        st.session_state.page = "manage"
        st.experimental_rerun()
