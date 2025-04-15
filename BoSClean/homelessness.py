import pandas as pd
import os
from IdMapping import clean_provider_ids

def clean_homelessness():
    """
    Cleans and summarizes homelessness data from the 'EE UDES' tab of all Excel files.
    Groups and counts values for:
    - Prior Living Situation
    - Times Homeless in 3 Years
    - Months Homeless in 3 Years
    Outputs three Excel sheets to the BoSClean folder.
    """
    
    folder_path = "./BoS (Business Objects) Raw Data Reports - Deidentified"
    output_path = "./BoSClean/homelessness_counts.xlsx"
    
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

            #  --- Process EE UDES Sheet ---
            try:
                df = pd.read_excel(file_path, sheet_name="EE UDES")
                # Clean EE Provider ID
                df = clean_provider_ids(df)
                df = df.rename(columns={'Prior Living Situation(43)': 'Prior Living Situation',
                                        'Regardless of where they stayed last night - Number of times the client has been on the streets, in ES, or SH in the past three years including today(12481)': 
                                        'Times Homeless in 3 years', 
                                        'Total number of months homeless on the street, in ES or SH in the past three years(12482)': 'Months Homeless in 3 years'})
                
                df["Months Homeless in 3 years"] = df["Months Homeless in 3 years"].replace({
                    "One month (this time is the first month) (HUD)": "1", 
                    "More than 12 months (HUD)": "More than 12"
                    })
                
                # Normalize HUD-coded values in Times Homeless in 3 Years
                df["Times Homeless in 3 years"] = df["Times Homeless in 3 years"].replace({
                    "One time (HUD)": "1",
                    "Two times (HUD)": "2",
                    "Three times (HUD)": "3",
                    "Four or more times (HUD)": ">=4"
                })
                
                df["Prior Living Situation"] = df["Prior Living Situation"].replace({
                    "Emergency shelter, including hotel or motel paid for with emergency shelter voucher, Host Home shelter (HUD)": "Emergency Shelter",
                    "Staying or living in a family member’s room, apartment, or house (HUD)": "Family's Home",
                    "Staying or living in a friend’s room, apartment, or house (HUD)": "Friend's Home",
                    "Safe Haven (HUD)": "Safe Haven",
                    "Place not meant for habitation (e.g., a vehicle, an abandoned building, bus/train/subway station/airport or anywhere outside) (HUD)": "Unsheltered",
                    "Rental by client, no ongoing housing subsidy (HUD)": "Rental (no subsidy)",
                    "Rental by client, with ongoing housing subsidy (HUD)": "Rental (with subsidy)",
                    "Foster care home or foster care group home (HUD)": "Foster Care",
                    "Other (HUD)": "Other",
                    "Transitional housing for homeless persons (including homeless youth) (HUD)": "Transitional Housing",
                    "Substance abuse treatment facility or detox center (HUD)": "Substance Abuse Facility",
                    "Hotel or motel paid for without emergency shelter voucher (HUD)": "Hotel (no voucher)",
                    "Hospital or other residential non-psychiatric medical facility (HUD)": "Medical Facility",
                    "Psychiatric hospital or other psychiatric facility (HUD)": "Psychiatric Facility",
                    "Jail, prison, or juvenile detention facility (HUD)": "Correctional Facility",
                    "Residential project or halfway house with no homeless criteria (HUD)": "Halfway House"
                })


                df = df.fillna("Not Specified")
                
                # Group by Provider Abbrev + Tree and count Disability Determination values
                prior_living_counts = df.groupby(["Provider Abbrev", "Provider Tree"])['Prior Living Situation'].value_counts(dropna=True).reset_index(name="Count")
                times_homeless_counts = df.groupby(["Provider Abbrev", "Provider Tree"])['Times Homeless in 3 years'].value_counts(dropna=True).reset_index(name="Count")
                months_homeless_counts = df.groupby(["Provider Abbrev", "Provider Tree"])['Months Homeless in 3 years'].value_counts(dropna=True).reset_index(name="Count")

                prior_living_allcounts.append(prior_living_counts)
                times_homeless_allcounts.append(times_homeless_counts)
                months_homeless_allcounts.append(months_homeless_counts)
            
            except Exception as e:
                print(f"Could not process Entry tab in {file}: {e}")


    # Write results to Excel
    with pd.ExcelWriter(output_path) as writer:
        if prior_living_allcounts:
            pd.concat(prior_living_allcounts, ignore_index=True).to_excel(writer, sheet_name='Prior Living', index=False)
        if times_homeless_allcounts:
            pd.concat(times_homeless_allcounts, ignore_index=True).to_excel(writer, sheet_name='Times Homeless', index=False)
        if months_homeless_allcounts:
            pd.concat(months_homeless_allcounts, ignore_index=True).to_excel(writer, sheet_name='Months Homeless', index=False)

    print(f"✅ Homelessness counts saved to: {output_path}")