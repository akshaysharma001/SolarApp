from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter, inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak


import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# GitHub file raw URL (replace with your GitHub raw file URL)
GITHUB_REPO_URL = "https://raw.githubusercontent.com/akshaysharma001/SolarApp/main/customer_data.xlsx"

# Function to load data from GitHub
def load_data():
    try:
        response = requests.get(GITHUB_REPO_URL)
        response.raise_for_status()
        file_content = BytesIO(response.content)
        return pd.read_excel(file_content)
    except Exception as e:
        st.error(f"Error loading data from GitHub: {str(e)}")
        # Return an empty DataFrame with predefined columns if file doesn't exist
        return pd.DataFrame(columns=[
            "date", "name", "address", "phone", "email", "panel_capacity",
            "solar_panel_company", "solar_panel_type", "solar_panel_category",
            "inverter_company", "inverter_category", "inverter_phase",
            "inverter_type", "mounting_roof", "mounting_material",
            "fixing_material", "earthing", "wiring", "dcdb_box",
            "acdb_box", "insulation_material", "panel_cleaning_system",
            "employee_name", "employee_email"
        ])

# Function to export the data to a PDF

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor  # Import HexColor for hex codes
from io import BytesIO
import streamlit as st

def export_to_pdf(data):
    try:
        # Create PDF output buffer
        pdf_output = BytesIO()
        pdf = SimpleDocTemplate(pdf_output, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=80, bottomMargin=30)
        elements = []

        # Title and header for invoice
        title = "Customer Invoice"
        subtitle = "Solar Panel Installation Details"

        # Company Information
        company_name = "SolarTech Solutions"
        company_address = "123 Solar St, Solar City, SC 12345"
        company_phone = "(123) 456-7890"
        company_email = "contact@solartech.com"

        # Define professional styles
        styles = getSampleStyleSheet()

        # Custom styles for the header
        header_title_style = ParagraphStyle(
            'HeaderTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=HexColor("#1877F2"),  # Facebook blue using HexColor
            alignment=1,  # Centered text
            spaceAfter=12,  # Space after title
            fontName="Helvetica-Bold"
        )
        header_subtitle_style = ParagraphStyle(
            'HeaderSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.black,
            alignment=1,  # Centered text
            spaceAfter=12,  # Space after subtitle
            fontName="Helvetica"
        )
        company_style = ParagraphStyle(
            'CompanyInfo',
            fontSize=12,
            textColor=colors.black,
            alignment=1,  # Centered text
            spaceAfter=6  # Space after company name/address
        )
        company_contact_style = ParagraphStyle(
            'CompanyContact',
            fontSize=10,
            textColor=colors.black,
            alignment=1,  # Centered text
            spaceAfter=18  # Space after contact info
        )

        # Add Title and Subtitle (using Paragraph for better styling)
        def add_header():
            elements.append(Paragraph(title, header_title_style))  # Title
            elements.append(Spacer(1, 6))  # Spacer between title and subtitle
            elements.append(Paragraph(subtitle, header_subtitle_style))  # Subtitle
            elements.append(Spacer(1, 12))  # Space between subtitle and company info

            # Add Company Info with customized styling
            elements.append(Paragraph(f"<b>{company_name}</b>", company_style))  # Company Name
            elements.append(Paragraph(company_address, company_style))  # Address
            elements.append(Paragraph(f"Phone: <b>{company_phone}</b>", company_contact_style))  # Phone
            elements.append(Paragraph(f"Email: <b>{company_email}</b>", company_contact_style))  # Email
            elements.append(Spacer(1, 24))  # Add space after company contact

        # Loop through each customer and add their details to the PDF
        for index, row in data.iterrows():
            if index > 0:
                elements.append(PageBreak())  # Start a new page for each customer

            # Add Header on each page
            add_header()

            # Add Customer Details (Name, Address, Email, etc.)
            elements.append(Paragraph("<b>Customer Details:</b>", styles['Heading3']))

            customer_details = [
                ("Date:", row['date']),
                ("Name:", row['name']),
                ("Address:", row['address']),
                ("Phone:", row['phone']),
                ("Email:", row['email']),
                ("Panel Capacity:", row['panel_capacity']),
                ("Solar Panel Company:", row['solar_panel_company']),
                ("Solar Panel Type:", row['solar_panel_type']),
                ("Solar Panel Category:", row['solar_panel_category']),
                ("Inverter Company:", row['inverter_company']),
                ("Inverter Category:", row['inverter_category']),
                ("Inverter Phase:", row['inverter_phase']),
                ("Inverter Type:", row['inverter_type']),
                ("Mounting Roof:", row['mounting_roof']),
                ("Mounting Material:", row['mounting_material']),
                ("Fixing Material:", row['fixing_material']),
                ("Earthing:", row['earthing']),
                ("Wiring:", row['wiring']),
                ("DCDB Box:", row['dcdb_box']),
                ("ACDB Box:", row['acdb_box']),
                ("Insulation Material:", row['insulation_material']),
                ("Panel Cleaning System:", row['panel_cleaning_system']),
                ("Employee Name:", row['employee_name']),
                ("Employee Email:", row['employee_email'])
            ]

            # Add a table for customer details to make it more structured
            table_data = []
            for label, value in customer_details:
                table_data.append([label, value])

            # Create table with styling
            table = Table(table_data, colWidths=[200, 300], rowHeights=30)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor("#1877F2")),  # Header Row Background
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header Row Text Color
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
            ]))

            elements.append(table)
            elements.append(Spacer(1, 24))  # Add space after table

        # Build the PDF
        pdf.build(elements)

        # Provide a download link
        st.success("PDF generated successfully! Click the button below to download it.")
        st.download_button(
            label="Download Invoice PDF",
            data=pdf_output.getvalue(),
            file_name="customer_invoice.pdf",
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"Error while generating PDF: {str(e)}")


# Load data
df = load_data()

# Normalize phone number column
df["phone"] = df["phone"].astype(str).str.strip()

# Streamlit app title
st.title("Customer Solar Panel Data Management System")

# Your existing Streamlit code follows...

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
             # Employee Name and Email fields - Filtered based on logged-in user
            if st.session_state.user_email == "admin":
                employee_names = df["employee_name"].unique()
                employee_emails = df["employee_email"].unique()
            else:
                # Filter employee by the logged-in user's email
                employee_names = df[df["employee_email"] == st.session_state.user_email]["employee_name"].unique()
                employee_emails = df[df["employee_email"] == st.session_state.user_email]["employee_email"].unique()

            # Employee dropdowns
            employee_name = st.selectbox("Employee Name", employee_names)
            employee_email = st.selectbox("Employee Email Address", employee_emails)

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

                    # Save DataFrame to Excel
                    #df.to_excel(GITHUB_REPO_URL, index=False)
                    df.to_excel("customer_data.xlsx", index=False)
                    st.success("Customer data saved successfully!")
    else:
        st.error("Please log in to add customer details.")

# Tab 2: Search Customer Details by Name
with tab2:
    if st.session_state.logged_in:
        st.header("Search Customer by Name")
        
        with st.form("search_form_name"):
            search_name = st.text_input("Enter Customer Name to Search")

            if st.form_submit_button("Search"):
                if search_name:
                    # Normalize search input
                    search_name = search_name.strip()

                    # Filter data by customer name, depending on the logged-in employee
                    if st.session_state.user_email == "admin":
                        result = df[df["name"].str.contains(search_name, case=False, na=False)]
                    else:
                        result = df[(df["name"].str.contains(search_name, case=False, na=False)) & (df["employee_email"] == st.session_state.user_email)]

                    if not result.empty:
                        # Store search results in session state
                        st.session_state.search_results = result
                        st.write("Customer Details:")
                        st.dataframe(result)
                    else:
                        st.warning("No records found for the given name.")
                else:
                    st.error("Please enter a name to search.")
        
        # Check if search results exist and show export button
        if "search_results" in st.session_state and not st.session_state.search_results.empty:
            if st.button("Export to PDF - Search by Name"):
                export_to_pdf(st.session_state.search_results)
    else:
        st.error("Please log in to search for customers.")

# Tab 3: Search Customer Details by Phone Number
with tab3:
    if st.session_state.logged_in:
        st.header("Search Customer by Phone Number")
        
        with st.form("search_form_phone"):
            search_phone = st.text_input("Enter Phone Number to Search")

            if st.form_submit_button("Search by Phone"):
                if search_phone:
                    # Normalize search input
                    search_phone = search_phone.strip()

                    # Filter data by phone number
                    if st.session_state.user_email == "admin":
                        result = df[df["phone"] == search_phone]
                    else:
                        result = df[(df["phone"] == search_phone) & (df["employee_email"] == st.session_state.user_email)]

                    if not result.empty:
                        # Store search results in session state
                        st.session_state.search_results = result
                        st.write("Customer Details:")
                        st.dataframe(result)
                    else:
                        st.warning("No records found for the given phone number.")
                else:
                    st.error("Please enter a phone number to search.")
        
        # Check if search results exist and show export button
        if "search_results" in st.session_state and not st.session_state.search_results.empty:
            if st.button("Export to PDF - Search by Phone"):
                export_to_pdf(st.session_state.search_results)
    else:
        st.error("Please log in to search for customers.")

# Tab 4: View All Records
with tab4:
    if st.session_state.logged_in:
        st.header("View All Customer Records")

        if st.session_state.user_email == "admin":
            result = df
        else:
            result = df[df["employee_email"] == st.session_state.user_email]

        # Display all records with an option to search by phone number
        st.dataframe(result)

        # Search by phone functionality
        search_phone_all = st.text_input("Search by Phone Number (for all records)")
        if search_phone_all:
            filtered_result = result[result["phone"].str.contains(search_phone_all, na=False)]
            st.dataframe(filtered_result)

        # Export to PDF for all records
        if st.session_state.user_email == "admin":
            # Export Button - Always Visible for Admin
            st.subheader("Export All Records to PDF")
            if st.button("Export All Records to PDF"):
                export_to_pdf(result)

# Tab 5: Admin Management Module
with st.sidebar:
    if st.session_state.logged_in and st.session_state.user_email == "admin":
        st.header("Admin Management")
        # Admin Management Module for updating and adding values to dropdowns
        tab5 = st.selectbox("Choose an action", ["Manage Dropdowns", "Manage Records"])
        
        if tab5 == "Manage Dropdowns":
            st.subheader("Manage Dropdown Options")

            # Panel Capacity Dropdown
            panel_capacity_options = ["1 KW", "2 KW", "5 KW", "10 KW"]
            new_panel_capacity = st.text_input("Add New Panel Capacity")
            if st.button("Add Panel Capacity Option"):
                if new_panel_capacity:
                    panel_capacity_options.append(new_panel_capacity)
                    st.success(f"Added '{new_panel_capacity}' to Panel Capacity options!")
            
            remove_panel_capacity = st.selectbox("Remove Panel Capacity Option", panel_capacity_options)
            if st.button("Remove Panel Capacity Option"):
                if remove_panel_capacity:
                    panel_capacity_options.remove(remove_panel_capacity)
                    st.success(f"Removed '{remove_panel_capacity}' from Panel Capacity options!")

            # Solar Panel Company Dropdown
            solar_panel_company_options = ["Company A", "Company B", "Company C"]
            new_solar_panel_company = st.text_input("Add New Solar Panel Company")
            if st.button("Add Solar Panel Company"):
                if new_solar_panel_company:
                    solar_panel_company_options.append(new_solar_panel_company)
                    st.success(f"Added '{new_solar_panel_company}' to Solar Panel Company options!")
            
            remove_solar_panel_company = st.selectbox("Remove Solar Panel Company", solar_panel_company_options)
            if st.button("Remove Solar Panel Company"):
                if remove_solar_panel_company:
                    solar_panel_company_options.remove(remove_solar_panel_company)
                    st.success(f"Removed '{remove_solar_panel_company}' from Solar Panel Company options!")

            # Similar logic can be added for other dropdowns like solar_panel_type, inverter_company, etc.

        elif tab5 == "Manage Records":
            st.subheader("Manage Customer Records")
            # Allow the admin to search and edit/delete customer records directly
            search_customer_by_name = st.text_input("Enter Customer Name to Edit/Delete")
            if st.button("Search Customer"):
                customer_found = df[df["name"].str.contains(search_customer_by_name, case=False, na=False)]
                if not customer_found.empty:
                    st.dataframe(customer_found)
                    # Provide options to edit or delete customer records here
                    selected_row = st.selectbox("Select Customer to Edit/Delete", customer_found.index.tolist())
                    if st.button("Delete Customer Record"):
                        df = df.drop(selected_row)
                        #df.to_excel(GITHUB_REPO_URL, index=False)
                        df.to_excel("customer_data.xlsx", index=False)
                        st.success("Customer record deleted successfully!")
                    if st.button("Edit Customer Record"):
                        st.warning("Edit functionality to be added.")
                else:
                    st.warning("Customer not found!")

    else:
        st.error("Please log in to view all customer records.")
