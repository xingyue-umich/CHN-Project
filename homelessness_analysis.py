import pandas as pd
import os

# Folder with all your Excel files
folder_path = "../BoS (Business Objects) Raw Data Reports - Deidentified"

# Loop through all Excel files in the folder
for file in os.listdir(folder_path):
    if file.endswith(".xlsx"):
        file_path = os.path.join(folder_path, file)
        program_name = file.split(" ")[0]  # Extract 'Program' from filename

# Read and process EE UDES sheet
        try:
            df = pd.read_excel(file_path, sheet_name="EE UDES")
            df = df.rename(columns={'Prior Living Situation(43)': 'Prior Living Situation','Regardless of where they stayed last night - Number of times the client has been on the streets, in ES, or SH in the past three years including today(12481)': 
                                    'Times Homeless (3 years)', 'Total number of months homeless on the street, in ES or SH in the past three years(12482)': 'Months Homeless (3 years)'})
            df["Months Homeless (3 years)"] = df["Months Homeless (3 years)"].replace({"One month (this time is the first month) (HUD)": "1", "More than 12 months (HUD)": "More than 12"})
            df = df.fillna("Not Specified")
            
            specified_columns = ['Prior Living Situation', 'Times Homeless (3 years)', 'Months Homeless (3 years)']
            df_selected = df[specified_columns]

            prior_living_counts = df_selected['Prior Living Situation'].value_counts(dropna=False).reset_index()
            prior_living_counts.columns = ['Prior Living Situation', 'Count']
            
            times_homeless_counts = df_selected['Times Homeless (3 years)'].value_counts(dropna=False).reset_index()
            times_homeless_counts.columns = ['Times Homeless (3 years)', 'Count']
            
            months_homeless_counts = df_selected['Months Homeless (3 years)'].value_counts(dropna=False).reset_index()
            months_homeless_counts.columns = ['Months Homeless (3 years)', 'Count']
        
        except Exception as e:
            print(f"Could not process Entry tab in {file}: {e}")

# Export all value counts to Excel in separate sheets
with pd.ExcelWriter("homelessness_value_counts.xlsx") as writer:
    prior_living_counts.to_excel(writer, sheet_name='Prior Living', index=False)
    times_homeless_counts.to_excel(writer, sheet_name='Times Homeless (3 years)', index=False)
    months_homeless_counts.to_excel(writer, sheet_name='Months Homeless (3 years)', index=False)
