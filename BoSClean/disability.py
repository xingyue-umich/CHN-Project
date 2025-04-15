import pandas as pd
import os
from IdMapping import clean_provider_ids

def clean_disability():
    folder_path = "./BoS (Business Objects) Raw Data Reports - Deidentified"
    output_path = "./BoSClean/disability_counts.xlsx"

    # Initialize a list to collect all counts
    all_counts = []

    # Loop through all Excel files in the folder
    for file in os.listdir(folder_path):
        
        if file == "TEMPLATE RAW Client Data Export v3_EE Workflow.xlsx":
            continue  # Skip this specific file
        
        if file.endswith(".xlsx"):
            file_path = os.path.join(folder_path, file)
            
            # --- Process DISABILITY ENT Sheet ---
            try:
                df_entry = pd.read_excel(file_path, sheet_name="DISABILITY ENT")
                df_entry_cleaned = clean_provider_ids(df_entry)  # Map and filter EE Provider IDs
                df_entry_cleaned.fillna("Not Specified")
                
                # Group by Provider Abbrev + Tree and count Disability Determination values
                grouped_entry = (
                    df_entry_cleaned
                    .groupby(["Provider Abbrev", "Provider Tree"])["Disability Determination (Entry)"]
                    .value_counts(dropna=True)
                    .reset_index(name="Count")
                )
                
                # Rename columns
                grouped_entry.rename(columns={"Disability Determination (Entry)": "Disability Status"}, inplace=True)
                grouped_entry["Assessment Stage"] = "Entry"
                all_counts.append(grouped_entry)
                
            except Exception as e:
                print(f"⚠️ Could not process Entry tab in {file}: {e}")

            # --- Process DISABILITY EXIT Sheet ---
            try:
                df_exit = pd.read_excel(file_path, sheet_name="DISABILITY EXIT")
                df_exit_cleaned = clean_provider_ids(df_exit)  # Map and filter EE Provider IDs
                df_exit_cleaned.fillna("Not Specified")
                
                # Group by Provider Abbrev + Tree and count Disability Determination values
                grouped_exit = (
                    df_exit_cleaned
                    .groupby(["Provider Abbrev", "Provider Tree"])["Disability Determination (Exit)"]
                    .value_counts(dropna=False)
                    .reset_index(name="Count")
                )
                grouped_exit.rename(columns={"Disability Determination (Exit)": "Disability Status"}, inplace=True)
                grouped_exit["Assessment Stage"] = "Exit"
                all_counts.append(grouped_exit)
                
            except Exception as e:
                print(f"⚠️ Could not process Exit tab in {file}: {e}")

    # Combine all results into a single DataFrame
    combined_df = pd.concat(all_counts, ignore_index=True)

    # Export to Excel
    combined_df.to_excel(output_path, index=False)

    print(f"✅ Combined disability counts saved to: {output_path}")