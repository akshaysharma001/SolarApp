import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# GitHub raw file URL (replace with your actual GitHub repository details)
GITHUB_REPO_URL = "https://raw.githubusercontent.com/akshaysharma001/SolarApp/new/customer_data.xlsx"

def load_data():
    """Loads data from the GitHub repository."""
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

def export_to_pdf(data):
    """Exports data to a PDF and allows download via Streamlit."""
    try:
        pdf_output = BytesIO()
        pdf = SimpleDocTemplate(pdf_output, pagesize=letter)
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

        st.success("PDF generated successfully! Click the button below to download it.")
        st.download_button(
            label="Download PDF",
            data=pdf_output.getvalue(),
            file_name="customer_records.pdf",
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"Error while generating PDF: {str(e)}")

def download_updated_excel(data):
    """Allows users to download updated Excel data for manual upload to GitHub."""
    try:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            data.to_excel(writer, index=False, sheet_name='Sheet1')
        st.download_button(
            label="Download Updated Excel File",
            data=output.getvalue(),
            file_name="updated_customer_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"Error while creating downloadable Excel file: {str(e)}")

# Load data from GitHub
df = load_data()

# Normalize phone number column
df["phone"] = df["phone"].astype(str).str.strip()

# Streamlit app title
st.title("Customer Solar Panel Data Management System")

# Add new customer details
with st.form("Add Customer"):
    st.subheader("Add New Customer")
    date = st.date_input("Date")
    name = st.text_input("Customer Name")
    address = st.text_area("Address")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    panel_capacity = st.number_input("Panel Capacity (kW)", min_value=0.0, step=0.1)
    solar_panel_company = st.text_input("Solar Panel Company")
    solar_panel_type = st.text_input("Solar Panel Type")
    solar_panel_category = st.text_input("Solar Panel Category")
    inverter_company = st.text_input("Inverter Company")
    inverter_category = st.text_input("Inverter Category")
    inverter_phase = st.text_input("Inverter Phase")
    inverter_type = st.text_input("Inverter Type")
    mounting_roof = st.text_input("Mounting Roof")
    mounting_material = st.text_input("Mounting Material")
    fixing_material = st.text_input("Fixing Material")
    earthing = st.text_input("Earthing")
    wiring = st.text_input("Wiring")
    dcdb_box = st.text_input("DCDB Box")
    acdb_box = st.text_input("ACDB Box")
    insulation_material = st.text_input("Insulation Material")
    panel_cleaning_system = st.text_input("Panel Cleaning System")
    employee_name = st.text_input("Employee Name")
    employee_email = st.text_input("Employee Email")
    submit = st.form_submit_button("Add Customer")

    if submit:
        new_row = {
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
            "employee_email": employee_email
        }
        df = df.append(new_row, ignore_index=True)
        st.success("Customer added successfully!")

# Display data
if not df.empty:
    st.subheader("Customer Records")
    st.dataframe(df)
    export_to_pdf(df)
    download_updated_excel(df)
else:
    st.warning("No customer data available.")
