import streamlit as st
import csv
import os
import io
import zipfile

def split_csv(input_file, output_prefix, rows_per_file):
    reader = csv.reader(io.StringIO(input_file.getvalue().decode('utf-8')))
    header = next(reader)  # Read the header row
    
    file_number = 1
    row_count = 0
    current_rows = []
    output_files = []
    
    for row in reader:
        current_rows.append(row)
        row_count += 1
        
        if row_count == rows_per_file:
            output_files.append((f"{output_prefix}{file_number}.csv", header, current_rows))
            file_number += 1
            row_count = 0
            current_rows = []
    
    # Write any remaining rows
    if current_rows:
        output_files.append((f"{output_prefix}{file_number}.csv", header, current_rows))
    
    return output_files

def create_zip(output_files):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_name, header, rows in output_files:
            csv_buffer = io.StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow(header)
            writer.writerows(rows)
            zip_file.writestr(file_name, csv_buffer.getvalue())
    return zip_buffer

st.title('CSV Splitter')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
rows_per_file = st.number_input("Number of rows per file", min_value=1, value=100)
output_prefix = st.text_input("Base name for output files", value="Unitedscientificsheet")

if uploaded_file is not None and st.button('Split CSV'):
    output_files = split_csv(uploaded_file, output_prefix, rows_per_file)
    
    zip_buffer = create_zip(output_files)
    
    st.success(f"CSV has been split into {len(output_files)} files.")
    
    st.download_button(
        label="Download ZIP file",
        data=zip_buffer.getvalue(),
        file_name="split_csv_files.zip",
        mime="application/zip"
    )