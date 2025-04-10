import pandas as pd
import datetime
import os

# Folder with all your Excel files
folder_path = "./BoS (Business Objects) Raw Data Reports - Deidentified"

# Initialize a list to collect all counts
all_counts = []

# Loop through all Excel files in the folder
for file in os.listdir(folder_path):
    
    if file == "TEMPLATE RAW Client Data Export v3_EE Workflow.xlsx":
        continue  # Skip this specific file
    
    if file.endswith(".xlsx"):
        file_path = os.path.join(folder_path, file)
        program_name = file.split(" ")[0]  # Extract 'Program' from filename

        # Read and process entry_exit sheet
        try:
            entry_exit = pd.read_excel(file_path, sheet_name="ENTRY-EXIT")
            
            # Convert to datetime
            entry_exit['Entry Date'] = pd.to_datetime(entry_exit['Entry Date'])
            entry_exit['Exit Date'] = pd.to_datetime(entry_exit['Exit Date'])

            # Fill missing Exit Date with current date (without time)
            today = pd.Timestamp.today().normalize()
            entry_exit['Exit Date'] = entry_exit['Exit Date'].fillna(today)

            # Create 'type' column
            entry_exit['type'] = entry_exit['Exit Date'].eq(today).map({True: 'Stayers', False: 'Leavers'})

            # Calculate 'Stay of length' in days
            entry_exit['Stay of length'] = (entry_exit['Exit Date'] - entry_exit['Entry Date']).dt.days

            # Keep only the 4 relevant columns
            entry_exit = entry_exit[['Entry Date', 'Exit Date', 'type', 'Stay of length']]
            
            entry_exit['Program'] = program_name
            
            # Mapping dictionary
            program_mapping = {
                'OC': 'Oakland PATH',
                'MC': 'Macomb PATH',
                'Eric': 'Erin Park',
                'SPC': 'Shelter Plus Care',
                '143': '143',
                '1371': '1371',
                '8319': '8319',
                '11495':'11495'
            }

            # Apply mapping to the 'program' column
            entry_exit['Program'] = entry_exit['Program'].map(program_mapping)
            
            all_counts.append(entry_exit)

        except Exception as e:
            print(f"⚠️ Could not process entry_exit tab in {file}: {e}")

# Combine all results into a single DataFrame
combined_df = pd.concat(all_counts, ignore_index=True)

# Export to Excel
combined_df.to_excel("./BoSClean/length_of_stay.xlsx", index=False)

print("✅ Combined disability counts saved to both CSV and Excel.")
