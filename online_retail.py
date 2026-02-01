import streamlit as st
import pandas as pd

st.set_page_config(page_title = "Online Retail Mini Dashboard", layout = "centered", page_icon = "📊")

st.markdown("""
<style>      
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF; color: #000000;
    }
            
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 2px solid #000000 !important;
    }
            
    h1, h2, h3, h4, label, p {
        color: #000000 !important;
        font-family: 'Inter',
        sans-serif; text-transform:
        uppercase; letter-spacing: 0.05em;
    }
            
    [data-testid="stSidebar"] .stButton>button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #000000;
        border-radius: 0px;
        width: 100%;
        font-weight: 800;
        transition: 0.3s all ease;
    }
            
    [data-testid="stSidebar"] .stButton>button:hover {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border-color: #000000;
    }
            
    div[data-testid="stForm"] .stButton>button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #000000;
        border-radius: 0px;
        width: 100%;
        padding: 0.8rem; 
        font-weight: 900;
        transition: 0.3s all ease;
    }
            
    div[data-testid="stForm"] .stButton>button:hover {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border-color: #000000;
    }
            
    div[data-testid="stForm"] {
        background-color: #FFFFFF;
        border: 2px solid #000000;
        border-radius: 0px;
        box-shadow: 10px 10px 0px #000000; 
        padding: 2.5rem;
    }
            
    div[data-testid="stTextInput"] input {
        background-color: #FFFFFF;
        color: #000000;
        border: 2px solid #000000;
        border-radius: 0px;
    }
            
    div[data-testid="stTextInput"] input:focus {
        border-color: #000000;
        box-shadow: 0 0 0 1px #000000;
    }
            
    div[data-testid="stNotification"] {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border-radius: 0px;
        border: 1px solid #000000;
    }
            
    hr {
        border: 1px solid #000000 !important;
    }       
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if not st.session_state.logged_in:
    col1,col2,col3 = st.columns([1,5,1])
    with col2:
        st.title("ONLINE RETAIL Dataset System", text_alignment = "center")
        st.header("LOGIN", text_alignment = "center")

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
                    st.rerun()

                elif username == "UserRIG" and password == "UserRIG456*@":
                    st.session_state.logged_in = True
                    st.session_state.page = "analysis"
                    st.session_state.role = "UserRIG"
                    st.success("✅ User Login successful")
                    st.rerun()

                else:
                    st.error(
                        "❌ Invalid username or password! "
                        "If you forgot the password, please contact your supervisor."
                    )
        st.stop()
else:
    with st.sidebar:
        st.title("WELCOME BACK👋🏼")
        st.info("You've logged into your account!")

        if st.button("Login", width="stretch"):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.rerun()

        if st.button("Logout", width="stretch"):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.rerun()

df = pd.read_excel("online_retail_mini.xlsx")
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["TotalSales"] = df["Quantity"]*df["Price"]

if st.session_state.page == "manage":
    st.title("Data Management Panel")
    action = st.selectbox("Choose Action",["Add Record", "Update Record", "Delete Record"])

    if action == "Add Record":
        with st.form("add_form"):
            invoice = st.text_input("Invoice No")
            country = st.text_input("Country")
            quantity = st.number_input("Quantity", min_value=1)
            price = st.number_input("Price", min_value = 0.0)
            date = st.date_input("Invoice Date")

            submit_add = st.form_submit_button("Add Record")
            if submit_add:
                new_row = {"Invoice": invoice, "Country": country, "Quantity": quantity, "Price": price, "InvoiceDate": date, "TotalSales": quantity * price}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index = True)
                df.to_excel("online_retail_mini.xlsx", index = False)
                st.success("✅ Record Added Successfully")

    elif action == "Update Record":
        invoice_list = df["Invoice"].astype(str).unique()
        selected_invoice = st.selectbox("Select Invoice", invoice_list)

        record = df[df["Invoice"].astype(str) == selected_invoice].iloc[0]

        with st.form("update_form"):
            quantity = st.number_input("Quantity", value = int(record["Quantity"]))
            price = st.number_input("Price", value = float(record["Price"]))
            submit_update = st.form_submit_button("Update Record")

            if submit_update:
                df.loc[df["Invoice"].astype(str) == selected_invoice, ["Quantity", "Price", "TotalSales"]] = [quantity, price, quantity * price]
                df.to_excel("online_retail_mini.xlsx", index = False)
                st.success("✅ Record Updated Successfully")

    elif action == "Delete Record":
        invoice_list = df["Invoice"].astype(str).unique()
        selected_invoice = st.selectbox("Select Invoice to Delete", invoice_list)

        if st.button("Delete Record"):
            df = df[df["Invoice"].astype(str) != selected_invoice]
            df.to_excel("online_retail_mini.xlsx", index=False)
            st.warning("🗑️ Record Deleted")

    st.divider()
    if st.button("➡️ Go to Analysis Dashboard"):
        st.session_state.page = "analysis"
        st.rerun()

if st.session_state.page != "analysis":
    st.stop()

with st.sidebar:
    st.title("Online Retail Dashboard")
    st.subheader("Settings")

    st.markdown("### Period")
    date_range=st.slider("Select Date Range", min_value=df["InvoiceDate"].min().date(), max_value=df["InvoiceDate"].max().date(), value=(df["InvoiceDate"].min().date(), df["InvoiceDate"].max().date()))

    st.markdown("### Country")
    country=st.multiselect("Select Country", df["Country"].dropna().unique(), default=df["Country"].dropna().unique())

filtered_df = df[
    (df["InvoiceDate"].dt.date >= date_range[0]) &
    (df["InvoiceDate"].dt.date <= date_range[1]) &
    (df["Country"].isin(country))
]

st.title("Online Retail Analysis Details")

row1=st.container()
with row1:
    st.header("RECORD DETAILS")
    col1,col2=st.columns(2)

    with col1:
        st.subheader("Total Sales by Country")
        sales_country=(filtered_df.groupby("Country")["TotalSales"].sum().reset_index())
        st.bar_chart(sales_country, x="Country", y="TotalSales", color="Country")

    with col2:
        st.subheader("Total Quantity Sold by Country")
        qty_country=(filtered_df.groupby("Country")["Quantity"].sum().reset_index())
        st.bar_chart(qty_country, x="Country", y="Quantity", color="Country")

row2=st.container()
with row2:
    st.header("SALES RELATIONSHIPS")
    col1,col2=st.columns(2)

    with col1:
        st.subheader("Price vs Quantity")
        st.scatter_chart(filtered_df, x="Price", y="Quantity", color="Country")

    with col2:
        st.subheader("Quantity vs Total Sales")
        st.scatter_chart(filtered_df, x="Quantity", y="TotalSales", color="Country")

row3=st.container()
with row3:
    st.header("TIME-BASED ANALYSIS")
    col1,col2=st.columns(2)

    with col1:
        st.subheader("Daily Total Sales")
        daily_sales=(filtered_df.groupby(filtered_df["InvoiceDate"].dt.date)["TotalSales"].sum().reset_index().set_index("InvoiceDate"))
        st.line_chart(daily_sales)

    with col2:
        st.subheader("Daily Total Quantity")
        daily_qty=(filtered_df.groupby(filtered_df["InvoiceDate"].dt.date)["Quantity"].sum().reset_index().set_index("InvoiceDate"))
        st.line_chart(daily_qty)

st.divider()
if st.session_state.role == "AdminRIG":
    if st.button("⬅️ Go Back to Data Management Panel"):
        st.session_state.page = "manage"
        st.rerun()