# %% [markdown]
# # IMPORTS AND SETUP

# %%
import pandas as pd  # For data manipulation and analysis, including working with DataFrames
import openpyxl as openxyl  # For reading and writing Excel files in .xlsx format
import os  # For interacting with the operating system, such as checking file existence
from datetime import datetime # For working with dates and times

# %%

# We define the folder path where our Excel files are stored
folder_path = "BoS (Business Objects) Raw Data Reports - Deidentified"

# %%
# Initialize an empty list to store all processed datasets
all_datasets = []

# Process each file in the directory
for file in os.listdir(folder_path):
    # Skip template files - this checks for any file with "TEMPLATE" in the name
    if "TEMPLATE" in file.upper():
        print(f"Skipping template file: {file}")
        continue
        
    # Only process Excel files
    if file.endswith(".xlsx"):
        try:
            # Construct the full file path
            file_path = os.path.join(folder_path, file)
            
            # Extract program ID from filename - adjust this based on your naming convention
            # This assumes filenames like "143 RAW Client Data Export v3_EE Workflow.xlsx"
            program_id = file.split(" RAW")[0]
            
            print(f"Processing file: {file} (Program ID: {program_id})")
            
            # Read the Excel file - the relevant data is in the "ENTRY-EXIT" sheet
            data_df = pd.read_excel(file_path, sheet_name="ENTRY-EXIT")
            
            # Process date columns to datetime format
            data_df['Entry Date'] = pd.to_datetime(data_df['Entry Date'], errors='coerce')
            data_df['Exit Date'] = pd.to_datetime(data_df['Exit Date'], errors='coerce')
            
            # Handle missing exit dates with a default value (in this case, the end date of the reporting period)
            default_exit_date = pd.to_datetime('09/30/2024 02:00:00')
            data_df['Exit Date'] = data_df['Exit Date'].fillna(default_exit_date)
            
            # Calculate Length of Stay in days
            data_df['Length of Stay'] = (data_df['Exit Date'] - data_df['Entry Date']).dt.days
            
            # Create new dataset with the columns we need
            new_dataset = pd.DataFrame({
                'Provider ID': data_df['EE Provider ID'],
                'Length of Stay': data_df['Length of Stay'],
                'Program': program_id
            })
            
            # Save individual program dataset
            output_path = f"./{program_id}.xlsx" # Save in the current directory
            new_dataset.to_excel(output_path, index=False)
            print(f"Created length_of_stay_{program_id}.xlsx")
            
            # Add to our collection for the combined file
            all_datasets.append(new_dataset)
            
        except Exception as e:
            print(f"Error processing file {file}: {e}")

# %%
# Combine all datasets into one file
if all_datasets:
    combined_dataset = pd.concat(all_datasets, ignore_index=True) 
    combined_path = "./length_of_stay_all_programs.xlsx"
    combined_dataset.to_excel(combined_path, index=False)
    print("Created combined file: length_of_stay_all_programs.xlsx")
else:
    print("No datasets were successfully processed.")


