import pandas as pd
import os

# Folder with all your Excel files
folder_path = "../BoS (Business Objects) Raw Data Reports - Deidentified"

# Initialize a list to collect all counts
all_counts = []

# Loop through all Excel files in the folder
for file in os.listdir(folder_path):
    if file.endswith(".xlsx"):
        file_path = os.path.join(folder_path, file)
        program_name = file.split(" ")[0]  # Extract 'Program' from filename

        # Read and process Entry sheet
        try:
            df_entry = pd.read_excel(file_path, sheet_name="DISABILITY ENT")
            entry_counts = df_entry['Disability Determination (Entry)'].value_counts(dropna=False).reset_index()
            entry_counts.columns = ['Disability Status', 'Count']
            entry_counts['Assessment Stage'] = 'Entry'
            entry_counts['Program'] = program_name
            all_counts.append(entry_counts)
        except Exception as e:
            print(f"⚠️ Could not process Entry tab in {file}: {e}")

        # Read and process Exit sheet
        try:
            df_exit = pd.read_excel(file_path, sheet_name="DISABILITY EXIT")
            exit_counts = df_exit['Disability Determination (Exit)'].value_counts(dropna=False).reset_index()
            exit_counts.columns = ['Disability Status', 'Count']
            exit_counts['Assessment Stage'] = 'Exit'
            exit_counts['Program'] = program_name
            all_counts.append(exit_counts)
        except Exception as e:
            print(f"⚠️ Could not process Exit tab in {file}: {e}")

# Combine all results into a single DataFrame
combined_df = pd.concat(all_counts, ignore_index=True)

# Export to Excel
# combined_df.to_csv("all_disability_counts.csv", index=False)
combined_df.to_excel("all_disability_counts.xlsx", index=False)

print("✅ Combined disability counts saved to both CSV and Excel.")
