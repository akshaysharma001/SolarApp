
import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# GitHub raw file URL (replace with your actual GitHub repository details)
GITHUB_REPO_URL = "https://raw.githubusercontent.com/akshaysharma001/SolarApp/main/customer_data.xlsx"

# Function to read data from GitHub
@st.cache_data
def load_data_from_github():
    try:
        response = requests.get(GITHUB_REPO_URL)
        response.raise_for_status()
        data = BytesIO(response.content)
        return pd.read_excel(data)
    except Exception as e:
        st.error(f"Error loading data from GitHub: {str(e)}")
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
def export_to_pdf(data):
    try:
        pdf_output_path = "customer_records.pdf"
        pdf = SimpleDocTemplate(pdf_output_path, pagesize=letter)
        elements = []

        data_list = data.values.tolist()
        columns = data.columns.tolist()
        data_table = [columns] + data_list

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

        with open(pdf_output_path, "rb") as file:
            st.download_button(
                label="Download PDF",
                data=file,
                file_name="customer_records.pdf",
                mime="application/pdf",
            )

    except Exception as e:
        st.error(f"Error while generating PDF: {str(e)}")

# Load data from GitHub
data = load_data_from_github()

# Streamlit app title
st.title("Customer Solar Panel Data Management System")

# Tabs for functionalities
tab1, tab2, tab3, tab4 = st.tabs(["Add Customer", "Search Customer by Name", "Search by Phone", "View All Records"])

# Tab 1: Add Customer
with tab1:
    st.header("Add Customer Details")
    with st.form("customer_form"):
        date = st.date_input("Date")
        name = st.text_input("Customer Name")
        address = st.text_area("Address")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email Address")

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
        employee_name = st.text_input("Employee Name")
        employee_email = st.text_input("Employee Email")

        submitted = st.form_submit_button("Save")

        if submitted:
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

            data = pd.concat([data, pd.DataFrame([new_entry])], ignore_index=True)
            st.success("Customer data saved successfully!")

# Tab 2: Search Customer by Name
with tab2:
    st.header("Search Customer by Name")
    search_name = st.text_input("Enter Customer Name")
    if st.button("Search by Name"):
        results = data[data["name"].str.contains(search_name, case=False, na=False)]
        if not results.empty:
            st.dataframe(results)
            if st.button("Export to PDF"):
                export_to_pdf(results)
        else:
            st.warning("No records found.")

# Tab 3: Search Customer by Phone
with tab3:
    st.header("Search Customer by Phone")
    search_phone = st.text_input("Enter Phone Number")
    if st.button("Search by Phone"):
        results = data[data["phone"].str.contains(search_phone, na=False)]
        if not results.empty:
            st.dataframe(results)
            if st.button("Export to PDF"):
                export_to_pdf(results)
        else:
            st.warning("No records found.")

# Tab 4: View All Records
with tab4:
    st.header("View All Records")
    st.dataframe(data)
    if st.button("Export All to PDF"):
        export_to_pdf(data)

# Note: Update your GitHub repository manually with the downloaded Excel file if changes are made.
