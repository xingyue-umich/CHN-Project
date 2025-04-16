import pandas as pd
import os
from IdMapping import clean_provider_ids

def calculate_permanent_exit():
    """
    Processes 'ENTRY-EXIT' sheets in Excel files to count exits to permanent vs. non-permanent housing.
    
    - Creates a 'permanent_housing' column based on the 'Destination' field
    - Tags each row as 'Yes' or 'No' based on known permanent housing destinations
    - Outputs a combined file with all rows and permanent housing classification
    """
    
    folder_path = "./BoS (Business Objects) Raw Data Reports - Deidentified"
    output_path = "./BoSClean/permanent_housing.xlsx"
    
    # Define what destinations are permanent
    permanent_housing_values = set([
    'Rental by client, with ongoing housing subsidy (HUD)',
    'Rental by client, no ongoing housing subsidy (HUD)',
    'Owned by client, no ongoing housing subsidy (HUD)',
    'Owned by client, with ongoing housing subsidy (HUD)',
    'Long-term care facility or nursing home (HUD)',
    'Staying or living with family, permanent tenure (HUD)',
    'Staying or living with friends, permanent tenure (HUD)'
    ])

    # Initialize lists to collect results
    permanent_housing_data = []

    # Loop through all Excel files in the folder
    for file in os.listdir(folder_path):
        
        if file == "TEMPLATE RAW Client Data Export v3_EE Workflow.xlsx":
            continue  # Skip this specific file
        
        if file.endswith(".xlsx"):
            file_path = os.path.join(folder_path, file)

            #  --- Process ENTRY-EXIT Sheet ---
            try:
                df = pd.read_excel(file_path, sheet_name="ENTRY-EXIT")
                # Clean EE Provider ID
                df = clean_provider_ids(df)
                
                if 'Destination' not in df.columns:
                    print(f"⚠️ Missing Destination column in {file}")
                    continue
                
                # Only include leavers
                df['Exit Date'] = pd.to_datetime(df.get('Exit Date'), errors='coerce')
                df = df[df['Exit Date'].notna()]

                df['Destination'] = df['Destination'].astype(str).str.strip()
                df['permanent_housing'] = df['Destination'].apply(
                    lambda x: 'Yes' if x in permanent_housing_values else 'No'
                )
                
                permanent_housing_data.append(
                    df[['Destination', 'permanent_housing', 'Provider Abbrev', 'Provider Tree']]
                )

            except Exception as e:
                print(f"⚠️ Could not process ENTRY-EXIT tab in {file}: {e}")
                
                
    if permanent_housing_data:
        combined_df = pd.concat(permanent_housing_data, ignore_index=True)
        combined_df.to_excel(output_path, index=False)
        print(f"✅ Permanent housing classification saved to: {output_path}")
    else:
        print("⚠️ No valid data found.")