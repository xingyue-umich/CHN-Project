import pandas as pd
import os
from IdMapping import clean_provider_ids

def clean_income():
    folder_path = "./BoS (Business Objects) Raw Data Reports - Deidentified"
    output_path = "./BoSClean/income_pct.xlsx"
    
    # Prompt user for date range
    try:
        start_date_input = input("Enter the start date (MM/DD/YYYY): ").strip()
        end_date_input = input("Enter the end date (MM/DD/YYYY): ").strip()

        start_date = pd.to_datetime(start_date_input, format="%m/%d/%Y")
        end_date = pd.to_datetime(end_date_input, format="%m/%d/%Y")

        if start_date > end_date:
            print("⚠️ Start date must be before end date.")
            return

    except Exception as e:
        print(f"⚠️ Invalid date format. Please use MM/DD/YYYY. Error: {e}")
        return
    
    # Initialize a list to collect all counts
    all_counts = []

    # Loop through all Excel files in the folder
    for file in os.listdir(folder_path):
        
        if file == "TEMPLATE RAW Client Data Export v3_EE Workflow.xlsx":
            continue  # Skip this specific file
        
        if file.endswith(".xlsx"):
            file_path = os.path.join(folder_path, file)
            
            # --- Process INCOME ENT and EXT Sheet ---
            try:
                income_ent = pd.read_excel(file_path, sheet_name='INCOME ENT')
                income_ext = pd.read_excel(file_path, sheet_name='INCOME EXT')
                
                # Clean EE Provider IDs (adds 'Provider Abbrev' and 'Provider Tree')
                income_ent = clean_provider_ids(income_ent)
                income_ext = clean_provider_ids(income_ext)
                
                income_ent['Income Start Date (Entry)'] = pd.to_datetime(
                    income_ent['Income Start Date (Entry)'], format='%m/%d/%Y', errors='coerce'
                )
                income_ent = income_ent[
                    (income_ent['Income Start Date (Entry)'] >= start_date) &
                    (income_ent['Income Start Date (Entry)'] <= end_date)
                ]

                income_ext['Income Start Date (Exit)'] = pd.to_datetime(
                    income_ext['Income Start Date (Exit)'], format='%m/%d/%Y', errors='coerce'
                )
                income_ext = income_ext[
                    (income_ext['Income Start Date (Exit)'] >= start_date) &
                    (income_ext['Income Start Date (Exit)'] <= end_date)
                ]
                
                # Group and calculate % of 'Yes' for ENTRY
                grouped_ent = (
                    income_ent
                    .groupby(["Provider Abbrev", "Provider Tree"])["Receiving Income (Entry)"]
                    .value_counts(normalize=True)
                    .rename("Percent")
                    .reset_index()
                )
                grouped_ent = grouped_ent[grouped_ent["Receiving Income (Entry)"] == "Yes"]
                grouped_ent = grouped_ent.rename(columns={"Receiving Income (Entry)": "Receiving Income"})
                grouped_ent["Percent"] = (grouped_ent["Percent"] * 100).round(2)
                grouped_ent["Assessment Stage"] = "Entry"

                # Group and calculate % of 'Yes' for EXIT
                grouped_ext = (
                    income_ext
                    .groupby(["Provider Abbrev", "Provider Tree"])["Receiving Income (Exit)"]
                    .value_counts(normalize=True)
                    .rename("Percent")
                    .reset_index()
                )
                
                grouped_ext = grouped_ext[grouped_ext["Receiving Income (Exit)"] == "Yes"]
                grouped_ext = grouped_ext.rename(columns={"Receiving Income (Exit)": "Receiving Income"})
                grouped_ext["Percent"] = (grouped_ext["Percent"] * 100).round(2)
                grouped_ext["Assessment Stage"] = "Exit"

                # Combine entry + exit, and tag with program name
                combined = pd.concat([grouped_ent, grouped_ext], ignore_index=True)
                all_counts.append(combined)
                
                
            except Exception as e:
                print(f"⚠️ Could not process Income tab in {file}: {e}")


    # Combine all programs and export
    combined_df = pd.concat(all_counts, ignore_index=True)
    combined_df.to_excel(output_path, index=False)

    print(f"✅ Income summary saved to: {output_path}")