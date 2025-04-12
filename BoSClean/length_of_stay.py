# %%
import pandas as pd
import openpyxl as openxyl

# %%
# # Load data specifically from the ENTRY-EXIT sheet
# data_143_df = pd.read_excel(
#     "/Users/natika/Downloads/past semesters/CHN-Project/BoS (Business Objects) Raw Data Reports - Deidentified/143 RAW Client Data Export v3_EE Workflow.xlsx", 
#     sheet_name="ENTRY-EXIT"
# )

# # Print columns to verify the data
# print(data_143_df.columns)

# %%
# # Convert date columns to datetime format
# data_143_df['Entry Date'] = pd.to_datetime(data_143_df['Entry Date'], errors='coerce')
# data_143_df['Exit Date'] = pd.to_datetime(data_143_df['Exit Date'], errors='coerce')

# # Fill missing Exit Date values with 09/30/2024
# default_exit_date = pd.to_datetime('09/30/2024 02:00:00')
# data_143_df['Exit Date'] = data_143_df['Exit Date'].fillna(default_exit_date)

# # Calculate the difference in days
# data_143_df['Length of Stay'] = (data_143_df['Exit Date'] - data_143_df['Entry Date']).dt.days

# # Display the first few rows of the DataFrame with the new column
# print(data_143_df[['Entry Date', 'Exit Date', 'Length of Stay']].head())

# %%

# Base directory
base_dir = "/Users/natika/Downloads/past semesters/CHN-Project/BoS (Business Objects) Raw Data Reports - Deidentified/"

# %%

import os

# List of program IDs to process
program_ids = ["143", "1371 FINAL", "8319", "11495", "Erin Park", "MC PATH", "OC PATH", "SPC"]  

# Initialize an empty list to store all processed datasets
all_datasets = []

# List of program IDs to process
program_ids = ["143", "1371 FINAL", "8319", "11495", "Erin Park", "MC PATH", "OC PATH", "SPC"]

# Initialize an empty list to store all processed datasets
all_datasets = []

# Process each program
for program_id in program_ids:
    # Construct file path
    file_path = f"{base_dir}{program_id} RAW Client Data Export v3_EE Workflow.xlsx"
    
    # Skip if filename contains the word "TEMPLATE"
    if "TEMPLATE" in file_path.upper():
        print(f"Skipping template file: {file_path}")
        continue
     # Verify that the file exists
    if not os.path.exists(file_path):
        print(f"Warning: File not found for program {program_id}: {file_path}")
        continue
    
    try:
        # Load data
        data_df = pd.read_excel(file_path, sheet_name="ENTRY-EXIT")
        
        # Convert date columns to datetime
        data_df['Entry Date'] = pd.to_datetime(data_df['Entry Date'], errors='coerce')
        data_df['Exit Date'] = pd.to_datetime(data_df['Exit Date'], errors='coerce')
        
        # Fill missing Exit Date values
        default_exit_date = pd.to_datetime('09/30/2024 02:00:00')
        data_df['Exit Date'] = data_df['Exit Date'].fillna(default_exit_date)
        
        # Calculate Length of Stay
        data_df['Length of Stay'] = (data_df['Exit Date'] - data_df['Entry Date']).dt.days
        
        # Create new dataset
        new_dataset = pd.DataFrame({
            'Length of Stay': data_df['EE Provider ID'],
            'Count': data_df['Length of Stay'],
            'Program': program_id
        })
        
        # Save individual dataset
        new_dataset.to_excel(f"/Users/natika/Downloads/past semesters/CHN-Project/length_of_stay_{program_id}.xlsx", index=False)
        print(f"Created length_of_stay_{program_id}.xlsx")
        
        # Add to our collection of all datasets
        all_datasets.append(new_dataset)
        
    except Exception as e:
        print(f"Error processing program {program_id}: {e}")

# Combine all datasets into one giant file
if all_datasets:
    combined_dataset_LOS = pd.concat(all_datasets, ignore_index=True)
    combined_dataset_LOS.to_excel("/Users/natika/Downloads/past semesters/CHN-Project/length_of_stay_all_programs.xlsx", index=False)
    print("Created combined file: length_of_stay_all_programs.xlsx")
else:
    print("No datasets were successfully processed.")


