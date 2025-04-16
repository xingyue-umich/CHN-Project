import pandas as pd
import os
from IdMapping import clean_provider_ids

def process_length_and_movein():
    """
    Processes Excel files to calculate:
    - Length of stay (Exit Date - Entry Date)
    - Days to housing move-in (Move-in Date - Entry Date)

    Results are saved to two sheets in the same Excel file:
    - 'Length_of_Stay'
    - 'Days_to_MoveIn'
    """
    
    folder_path = "./BoS (Business Objects) Raw Data Reports - Deidentified"
    output_path = "./BoSClean/housing_timelines.xlsx"
    
    # Initialize lists to collect results
    length_of_stay = []
    days_to_movein = []

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
                
                if 'Entry Date' not in df.columns or 'Exit Date' not in df.columns:
                    print(f"⚠️ Missing Entry/Exit Date columns in {file}")
                    continue
                
                # Process date columns to datetime format
                df['Entry Date'] = pd.to_datetime(df['Entry Date'], errors='coerce')
                df['Exit Date'] = pd.to_datetime(df['Exit Date'], errors='coerce')
                
                df.rename(columns={'Housing Move-in Date(12855)': 'Housing Move-in Date'}, inplace=True)
                df['Housing Move-in Date'] = pd.to_datetime(df.get('Housing Move-in Date'), errors='coerce')
                
                # Length of Stay
                # Handle missing exit dates with a default value (in this case, the end date of the reporting period)
                default_exit_date = pd.to_datetime('2024-09-30')
                df['Exit Date'] = df['Exit Date'].fillna(default_exit_date)
                df['Length of Stay'] = (df['Exit Date'] - df['Entry Date']).dt.days
                length_of_stay.append(df[['Entry Date', 'Exit Date', 'Length of Stay', 'Provider Abbrev', 'Provider Tree']])

                # Days to Housing Move-In
                df['Days_to_MoveIn'] = (df['Housing Move-in Date'] - df['Entry Date']).dt.days
                # Filter for valid move in data
                valid_cases = df[
                    (df['Days_to_MoveIn'] > 0) & 
                    (df['Housing Move-in Date'].notna())
                ]
                days_to_movein.append(valid_cases[['Entry Date', 'Housing Move-in Date', 'Days_to_MoveIn', 'Provider Abbrev', 'Provider Tree']])

            except Exception as e:
                print(f"⚠️ Could not process Entry-Exit tab in {file}: {e}")
                
    if length_of_stay or days_to_movein:
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            if length_of_stay:
                pd.concat(length_of_stay, ignore_index=True).to_excel(writer, sheet_name='Length_of_Stay', index=False)
            if days_to_movein:
                pd.concat(days_to_movein, ignore_index=True).to_excel(writer, sheet_name='Days_to_MoveIn', index=False)
        print(f"✅ Length of Stay and Days-to-movein results saved to: {output_path}")
    else:
        print("⚠️ No valid data found.")