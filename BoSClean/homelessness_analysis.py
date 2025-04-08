import pandas as pd
import os

# Folder with all your Excel files
folder_path = "./BoS (Business Objects) Raw Data Reports - Deidentified"

# Initialize lists to collect all counts
prior_living_allcounts = []
times_homeless_allcounts = []
months_homeless_allcounts = []

# Loop through all Excel files in the folder
for file in os.listdir(folder_path):
    
    if file == "TEMPLATE RAW Client Data Export v3_EE Workflow.xlsx":
        continue  # Skip this specific file 
    
    if file.endswith(".xlsx"):
        file_path = os.path.join(folder_path, file)
        program_name = file.split(" ")[0]  # Extract 'Program' from filename

# Read and process EE UDES sheet
        try:
            df = pd.read_excel(file_path, sheet_name="EE UDES")
            df = df.rename(columns={'Prior Living Situation(43)': 'Prior Living Situation','Regardless of where they stayed last night - Number of times the client has been on the streets, in ES, or SH in the past three years including today(12481)': 
                                    'Times Homeless in 3 years', 'Total number of months homeless on the street, in ES or SH in the past three years(12482)': 'Months Homeless in 3 years'})
            df["Months Homeless in 3 years"] = df["Months Homeless in 3 years"].replace({"One month (this time is the first month) (HUD)": "1", "More than 12 months (HUD)": "More than 12"})
            df = df.fillna("Not Specified")
            
            specified_columns = ['Prior Living Situation', 'Times Homeless in 3 years', 'Months Homeless in 3 years']
            df_selected = df[specified_columns]

            prior_living_counts = df_selected['Prior Living Situation'].value_counts(dropna=False).reset_index()
            prior_living_counts.columns = ['Prior Living Situation', 'Count']
            prior_living_counts['Program'] = program_name
            prior_living_allcounts.append(prior_living_counts)
            
            times_homeless_counts = df_selected['Times Homeless in 3 years'].value_counts(dropna=False).reset_index()
            times_homeless_counts.columns = ['Times Homeless in 3 years', 'Count']
            times_homeless_counts['Program'] = program_name
            times_homeless_allcounts.append(times_homeless_counts)
            
            months_homeless_counts = df_selected['Months Homeless in 3 years'].value_counts(dropna=False).reset_index()
            months_homeless_counts.columns = ['Months Homeless in 3 years', 'Count']
            months_homeless_counts['Program'] = program_name
            months_homeless_allcounts.append(months_homeless_counts)
        
        except Exception as e:
            print(f"Could not process Entry tab in {file}: {e}")


# Combine all results into a single DataFrame
prior_living_combined = pd.concat(prior_living_allcounts, ignore_index=True)
times_homeless_combined = pd.concat(times_homeless_allcounts, ignore_index=True)
months_homeless_combined = pd.concat(months_homeless_allcounts, ignore_index=True)

# Export all value counts to Excel in separate sheets
with pd.ExcelWriter("./BoSClean/homelessness.xlsx") as writer:
    prior_living_combined.to_excel(writer, sheet_name='Prior Living', index=False)
    times_homeless_combined.to_excel(writer, sheet_name='Times Homeless in 3 years', index=False)
    months_homeless_combined.to_excel(writer, sheet_name='Months Homeless in 3 years', index=False)