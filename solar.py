import os 
os.system('pip install reportlab')
import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# GitHub repository details
GITHUB_REPO = "akshaysharma001/SolarApp"
#GITHUB_FILE_PATH = "path/to/your/customer_data.xlsx"
GITHUB_API_URL = f"https://api.github.com/repos/akshaysharma001/contents/Solar.py"

GITHUB_FILE_PATH = "https://raw.githubusercontent.com/akshaysharma001/SolarApp/main/customer_data.xlsx"



# Function to fetch file content from GitHub
def get_github_file_content():
    response = requests.get(GITHUB_API_URL)
    if response.status_code == 200:
        file_content = response.json()['content']
        file_data = BytesIO(requests.utils.base64_b64decode(file_content))
        return pd.read_excel(file_data)
    else:
        st.error("Error fetching file from GitHub.")
        return pd.DataFrame()

# Function to upload file to GitHub
def upload_to_github(file_content, commit_message="Update file"):
    headers = {
        "Authorization": "Bearer YOUR_GITHUB_TOKEN",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get(GITHUB_API_URL)
    if response.status_code == 200:
        sha = response.json()['sha']
    else:
        sha = None

    upload_url = GITHUB_API_URL
    data = {
        "message": commit_message,
        "content": requests.utils.base64_b64encode(file_content).decode(),
        "sha": sha,
    }
    response = requests.put(upload_url, headers=headers, json=data)

    if response.status_code == 201:
        st.success("File uploaded successfully!")
    else:
        st.error("Error uploading file to GitHub.")

# Function to export the data to a PDF
def export_to_pdf(data):
    try:
        # Update PDF path
        pdf_output_path = "/tmp/customer_records.pdf"  # This will save the PDF in the Streamlit app's temporary directory

        # Create PDF document using SimpleDocTemplate (tabular format)
        pdf = SimpleDocTemplate(pdf_output_path, pagesize=letter)
        elements = []

        # Prepare data for the table
        data_list = data.values.tolist()
        columns = data.columns.tolist()
        data_table = [columns] + data_list

        # Create table
        table = Table(data_table)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))

        elements.append(table)
        pdf.build(elements)

        st.success(f"PDF saved successfully! You can download it from [here](file:///{pdf_output_path})")

    except Exception as e:
        st.error(f"Error while generating PDF: {str(e)}")


# Get the customer data from GitHub
df = get_github_file_content()
# Normalize phone number column


# Check if DataFrame is empty
if df.empty:
    st.error("No customer data found.")
else:
    # Check if 'phone' column exists before normalizing
    if "phone" in df.columns:
        df["phone"] = df["phone"].astype(str).str.strip()
    else:
        st.warning("'phone' column is missing in the data.")



df["phone"] = df["phone"].astype(str).str.strip()

# Streamlit app title
st.title("Customer Solar Panel Data Management System")

# Initialize session state to store search results and user information
if "search_results" not in st.session_state:
    st.session_state.search_results = pd.DataFrame()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""

# Login Form
if not st.session_state.logged_in:
    st.sidebar.header("Login")
    user_email = st.sidebar.text_input("Enter your Email ID")
    login_button = st.sidebar.button("Login")
    
    if login_button:
        # Check for valid user (Here you can validate against a pre-defined list of users or a database)
        admin_email = "admin@example.com"
        if user_email == admin_email:
            st.session_state.logged_in = True
            st.session_state.user_email = "admin"
            st.success("Logged in as Admin!")
        elif user_email != "":
            # Assuming employee records are associated with their email
            if user_email in df['employee_email'].values:
                st.session_state.logged_in = True
                st.session_state.user_email = user_email
                st.success(f"Logged in as {user_email}")
            else:
                st.error("Invalid Email ID")
else:
    # Display user-specific message
    st.sidebar.write(f"Logged in as: {st.session_state.user_email}")
    
    # Logout Button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.success("Logged out successfully!")

# Tabs for different functionalities
tab1, tab2, tab3, tab4 = st.tabs(["Add Customer", "Search Customer by Name", "Search by Phone Number", "View All Records"])

# Tab 1: Add Customer Details
with tab1:
    if st.session_state.logged_in:
        with st.form("customer_form"):
            st.header("Enter Customer Details")

            # Form fields
            date = st.date_input("Date")
            name = st.text_input("Customer Name")
            address = st.text_area("Address")
            phone = st.text_input("Phone Number")
            email = st.text_input("Email Address")

            # Dropdown fields
            panel_capacity = st.selectbox("Panel Capacity (KWH)", ["1 KW", "2 KW", "5 KW", "10 KW"])
            solar_panel_company = st.selectbox("Solar Panel Company", ["Company A", "Company B", "Company C"])
            solar_panel_type = st.selectbox("Solar Panel Type", ["Type 1", "Type 2", "Type 3"])
            solar_panel_category = st.selectbox("Solar Panel Category", ["Category 1", "Category 2", "Category 3"])
            inverter_company = st.selectbox("Inverter Company", ["Inverter Co A", "Inverter Co B", "Inverter Co C"])
            inverter_category = st.selectbox("Inverter Category", ["Category A", "Category B", "Category C"])
            inverter_phase = st.selectbox("Inverter Phase", ["Single Phase", "Three Phase"])
            inverter_type = st.selectbox("Inverter Type", ["Type A", "Type B"])
            mounting_roof = st.selectbox("Mounting Roof", ["Flat Roof", "Sloped Roof"])
            mounting_material = st.selectbox("Mounting Material", ["Material A", "Material B"])
            fixing_material = st.selectbox("Fixing Material", ["Material X", "Material Y"])
            earthing = st.selectbox("Earthing", ["Earthing Type 1", "Earthing Type 2"])
            wiring = st.selectbox("Wiring", ["Wiring Type A", "Wiring Type B"])
            dcdb_box = st.selectbox("DCDB Box", ["DCDB Type 1", "DCDB Type 2"])
            acdb_box = st.selectbox("ACDB Box", ["ACDB Type 1", "ACDB Type 2"])
            insulation_material = st.selectbox("Insulation Material", ["Material 1", "Material 2"])
            panel_cleaning_system = st.selectbox("Panel Cleaning System", ["System A", "System B"])
            employee_name = st.selectbox("Employee Name", ["Employee 1", "Employee 2", "Employee 3"])
            employee_email = st.selectbox("Employee Email Address", ["emp1@example.com", "emp2@example.com", "emp3@example.com"])

            # Form submission
            submitted = st.form_submit_button("Save")

            if submitted:
                # Ensure the employee_email is the logged-in user email
                if st.session_state.user_email != "admin" and st.session_state.user_email != employee_email:
                    st.error("You can only add customers for your own account.")
                else:
                    # Create a new entry
                    new_entry = {
                        "date": date,
                        "name": name,
                        "address": address,
                        "phone": phone,
                        "email": email,
                        "panel_capacity": panel_capacity,
                        "solar_panel_company": solar_panel_company,
                        "solar_panel_type": solar_panel_type,
                        "solar_panel_category": solar_panel_category,
                        "inverter_company": inverter_company,
                        "inverter_category": inverter_category,
                        "inverter_phase": inverter_phase,
                        "inverter_type": inverter_type,
                        "mounting_roof": mounting_roof,
                        "mounting_material": mounting_material,
                        "fixing_material": fixing_material,
                        "earthing": earthing,
                        "wiring": wiring,
                        "dcdb_box": dcdb_box,
                        "acdb_box": acdb_box,
                        "insulation_material": insulation_material,
                        "panel_cleaning_system": panel_cleaning_system,
                        "employee_name": employee_name,
                        "employee_email": employee_email,
                    }

                    # Append to DataFrame using pd.concat()
                    new_row_df = pd.DataFrame([new_entry])
                    df = pd.concat([df, new_row_df], ignore_index=True)

                    # Save DataFrame to GitHub
                    file_content = df.to_excel(index=False)
                    upload_to_github(file_content)
                    st.success("Customer data saved successfully!")
    else:
        st.error("Please log in to add customer details.")

# Tabs for the other functionalities (search, view all records, etc.) will be similar, making sure that file updates and reading from GitHub are handled accordingly.



# Tabs for different functionalities
tab1, tab2, tab3, tab4 = st.tabs(["Add Customer", "Search Customer by Name", "Search by Phone Number", "View All Records"])

# Tab 1: Add Customer Details
with tab1:
    if st.session_state.logged_in:
        with st.form("customer_form"):
            st.header("Enter Customer Details")

            # Form fields
            date = st.date_input("Date")
            name = st.text_input("Customer Name")
            address = st.text_area("Address")
            phone = st.text_input("Phone Number")
            email = st.text_input("Email Address")

            # Dropdown fields
            panel_capacity = st.selectbox("Panel Capacity (KWH)", ["1 KW", "2 KW", "5 KW", "10 KW"])
            solar_panel_company = st.selectbox("Solar Panel Company", ["Company A", "Company B", "Company C"])
            solar_panel_type = st.selectbox("Solar Panel Type", ["Type 1", "Type 2", "Type 3"])
            solar_panel_category = st.selectbox("Solar Panel Category", ["Category 1", "Category 2", "Category 3"])
            inverter_company = st.selectbox("Inverter Company", ["Inverter Co A", "Inverter Co B", "Inverter Co C"])
            inverter_category = st.selectbox("Inverter Category", ["Category A", "Category B", "Category C"])
            inverter_phase = st.selectbox("Inverter Phase", ["Single Phase", "Three Phase"])
            inverter_type = st.selectbox("Inverter Type", ["Type A", "Type B"])
            mounting_roof = st.selectbox("Mounting Roof", ["Flat Roof", "Sloped Roof"])
            mounting_material = st.selectbox("Mounting Material", ["Material A", "Material B"])
            fixing_material = st.selectbox("Fixing Material", ["Material X", "Material Y"])
            earthing = st.selectbox("Earthing", ["Earthing Type 1", "Earthing Type 2"])
            wiring = st.selectbox("Wiring", ["Wiring Type A", "Wiring Type B"])
            dcdb_box = st.selectbox("DCDB Box", ["DCDB Type 1", "DCDB Type 2"])
            acdb_box = st.selectbox("ACDB Box", ["ACDB Type 1", "ACDB Type 2"])
            insulation_material = st.selectbox("Insulation Material", ["Material 1", "Material 2"])
            panel_cleaning_system = st.selectbox("Panel Cleaning System", ["System A", "System B"])
            employee_name = st.selectbox("Employee Name", ["Employee 1", "Employee 2", "Employee 3"])
            employee_email = st.selectbox("Employee Email Address", ["emp1@example.com", "emp2@example.com", "emp3@example.com"])

            # Form submission
            submitted = st.form_submit_button("Save")

            if submitted:
                # Ensure the employee_email is the logged-in user email
                if st.session_state.user_email != "admin" and st.session_state.user_email != employee_email:
                    st.error("You can only add customers for your own account.")
                else:
                    # Create a new entry
                    new_entry = {
                        "date": date,
                        "name": name,
                        "address": address,
                        "phone": phone,
                        "email": email,
                        "panel_capacity": panel_capacity,
                        "solar_panel_company": solar_panel_company,
                        "solar_panel_type": solar_panel_type,
                        "solar_panel_category": solar_panel_category,
                        "inverter_company": inverter_company,
                        "inverter_category": inverter_category,
                        "inverter_phase": inverter_phase,
                        "inverter_type": inverter_type,
                        "mounting_roof": mounting_roof,
                        "mounting_material": mounting_material,
                        "fixing_material": fixing_material,
                        "earthing": earthing,
                        "wiring": wiring,
                        "dcdb_box": dcdb_box,
                        "acdb_box": acdb_box,
                        "insulation_material": insulation_material,
                        "panel_cleaning_system": panel_cleaning_system,
                        "employee_name": employee_name,
                        "employee_email": employee_email,
                    }

                    # Append to DataFrame using pd.concat()
                    new_row_df = pd.DataFrame([new_entry])
                    df = pd.concat([df, new_row_df], ignore_index=True)

                    # Save DataFrame to GitHub
                    file_content = df.to_excel(index=False)
                    upload_to_github(file_content)
                    st.success("Customer data saved successfully!")
    else:
        st.error("Please log in to add customer details.")

# Tabs for the other functionalities (search, view all records, etc.) will be similar, making sure that file updates and reading from GitHub are handled accordingly.
