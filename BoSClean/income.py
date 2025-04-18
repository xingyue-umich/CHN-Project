import pandas as pd
import os
from IdMapping import clean_provider_ids
from add_UID import add_uid_column

def clean_income():
    folder_path = "./BoS (Business Objects) Raw Data Reports - Deidentified"
    output_path = "./BoSClean/income_summary.xlsx"
    
    # Initialize a list to collect all counts
    all_pct = []
    all_counts = []
    noncash_results = []
    income_medians = []

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
                
                # --- PERCENTAGE ---
                # Group and calculate % of 'Yes' for ENTRY
                grouped_ent_pct = (
                    income_ent
                    .groupby(["Provider Abbrev", "Provider Tree"])["Receiving Income (Entry)"]
                    .value_counts(normalize=True)
                    .rename("Percent")
                    .reset_index()
                )
                grouped_ent_pct = grouped_ent_pct[grouped_ent_pct["Receiving Income (Entry)"] == "Yes"]
                grouped_ent_pct = grouped_ent_pct.rename(columns={"Receiving Income (Entry)": "Receiving Income"})
                grouped_ent_pct["Percent"] = (grouped_ent_pct["Percent"] * 100).round(2)
                grouped_ent_pct["Assessment Stage"] = "Entry"

                # Group and calculate % of 'Yes' for EXIT
                grouped_ext_pct = (
                    income_ext
                    .groupby(["Provider Abbrev", "Provider Tree"])["Receiving Income (Exit)"]
                    .value_counts(normalize=True)
                    .rename("Percent")
                    .reset_index()
                )
                grouped_ext_pct = grouped_ext_pct[grouped_ext_pct["Receiving Income (Exit)"] == "Yes"]
                grouped_ext_pct = grouped_ext_pct.rename(columns={"Receiving Income (Exit)": "Receiving Income"})
                grouped_ext_pct["Percent"] = (grouped_ext_pct["Percent"] * 100).round(2)
                grouped_ext_pct["Assessment Stage"] = "Exit"

                combined_pct = pd.concat([grouped_ent_pct, grouped_ext_pct], ignore_index=True)
                # add UID
                combined_pct = add_uid_column(combined_pct)
                all_pct.append(combined_pct)
                
                # --- COUNTS ---
                grouped_ent_count = (
                    income_ent
                    .groupby(["Provider Abbrev", "Provider Tree"])["Receiving Income (Entry)"]
                    .value_counts()
                    .rename("Count")
                    .reset_index()
                )
                grouped_ent_count["Assessment Stage"] = "Entry"

                grouped_ext_count = (
                    income_ext
                    .groupby(["Provider Abbrev", "Provider Tree"])["Receiving Income (Exit)"]
                    .value_counts()
                    .rename("Count")
                    .reset_index()
                )
                grouped_ext_count["Assessment Stage"] = "Exit"

                grouped_ent_count = grouped_ent_count.rename(columns={"Receiving Income (Entry)": "Receiving Income"})
                grouped_ext_count = grouped_ext_count.rename(columns={"Receiving Income (Exit)": "Receiving Income"})

                combined_count = pd.concat([grouped_ent_count, grouped_ext_count], ignore_index=True)
                # add UID
                combined_count = add_uid_column(combined_count)
                all_counts.append(combined_count)
                
                # === Income medians ===
                income_ent["Monthly Income (Start)"] = pd.to_numeric(income_ent["Monthly Income (Start)"], errors='coerce')
                income_ext["Monthly Income Amount (Exit)"] = pd.to_numeric(income_ext["Monthly Income Amount (Exit)"], errors='coerce')
                
                median_ent = (
                    income_ent
                    .groupby(["Provider Abbrev", "Provider Tree"])["Monthly Income (Start)"]
                    .median()
                    .reset_index()
                    .rename(columns={"Monthly Income (Start)": "Median Income"})
                )
                median_ent["Assessment Stage"] = "Entry"

                median_ext = (
                    income_ext
                    .groupby(["Provider Abbrev", "Provider Tree"])["Monthly Income Amount (Exit)"]
                    .median()
                    .reset_index()
                    .rename(columns={"Monthly Income Amount (Exit)": "Median Income"})
                )
                median_ext["Assessment Stage"] = "Exit"
                # add UID
                median_ent = add_uid_column(median_ent)
                median_ext = add_uid_column(median_ext)
                income_medians.append(pd.concat([median_ent, median_ext], ignore_index=True))

                # === NON-CASH ===
                noncash_ent = pd.read_excel(file_path, sheet_name='NONCASH ENT')
                noncash_ext = pd.read_excel(file_path, sheet_name='NONCASH EXIT')
                
                # Clean provider IDs
                noncash_ent = clean_provider_ids(noncash_ent)
                noncash_ext = clean_provider_ids(noncash_ext)

                # === Grouped Percentage of YES by Provider ===
                grouped_ent_noncash = (
                    noncash_ent
                    .groupby(["Provider Abbrev", "Provider Tree"])["Receiving Benefit (Entry)"]
                    .value_counts(normalize=True)
                    .rename("Percent")
                    .reset_index()
                )
                grouped_ent_noncash = grouped_ent_noncash[grouped_ent_noncash["Receiving Benefit (Entry)"] == "Yes"]
                grouped_ent_noncash = grouped_ent_noncash.rename(columns={"Receiving Benefit (Entry)": "Receiving Benefit"})
                grouped_ent_noncash["Percent"] = (grouped_ent_noncash["Percent"] * 100).round(2)
                grouped_ent_noncash["Assessment Stage"] = "Entry"

                grouped_ext_noncash = (
                    noncash_ext
                    .groupby(["Provider Abbrev", "Provider Tree"])["Receiving Benefit (Exit)"]
                    .value_counts(normalize=True)
                    .rename("Percent")
                    .reset_index()
                )
                grouped_ext_noncash = grouped_ext_noncash[grouped_ext_noncash["Receiving Benefit (Exit)"] == "Yes"]
                grouped_ext_noncash = grouped_ext_noncash.rename(columns={"Receiving Benefit (Exit)": "Receiving Benefit"})
                grouped_ext_noncash["Percent"] = (grouped_ext_noncash["Percent"] * 100).round(2)
                grouped_ext_noncash["Assessment Stage"] = "Exit"

                # Combine and append to master results
                combined_noncash_pct = pd.concat([grouped_ent_noncash, grouped_ext_noncash], ignore_index=True)
                combined_noncash_pct = add_uid_column(combined_noncash_pct)
                noncash_results.append(combined_noncash_pct)

            except Exception as e:
                print(f"⚠️ Could not process data in {file}: {e}")

    # Export both PCT and COUNT to different sheets
    with pd.ExcelWriter(output_path) as writer:
        if all_pct:
            pd.concat(all_pct, ignore_index=True).to_excel(writer, sheet_name='income pct', index=False)
        if all_counts:
            pd.concat(all_counts, ignore_index=True).to_excel(writer, sheet_name='income count', index=False)
        if noncash_results:
            pd.concat(noncash_results, ignore_index=True).to_excel(writer, sheet_name='noncash pct', index=False)
        if income_medians:
            pd.concat(income_medians, ignore_index=True).to_excel(writer, sheet_name='income median', index=False)


    print(f"✅ Income summary saved to: {output_path}")