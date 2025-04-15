# %%
import os
import pandas as pd

folder_path = "BoS (Business Objects) Raw Data Reports - Deidentified"


# %% [markdown]
# ### Number of clients who exited to permanent housing
# 

# %%
# Define permanent housing values to count
permanent_housing_values = [
    'Rental by client, with ongoing housing subsidy (HUD)',
    'Rental by client, no ongoing housing subsidy (HUD)',
    'Owned by client, no ongoing housing subsidy (HUD)',
    'Staying or living with family, permanent tenure (HUD)',
    'Staying or living with friends, permanent tenure (HUD)'
]

# Process each file in the folder
for file in os.listdir(folder_path):
    if file == "TEMPLATE RAW Client Data Export v3_EE Workflow.xlsx":
        continue  # Skip this specific file
    
    if file.endswith(".xlsx"):
        file_path = os.path.join(folder_path, file)
        
        try:
            # Load the dataframe for this file
            df_housing = pd.read_excel(file_path, sheet_name="ENTRY-EXIT")
            total_clients = len(df_housing)
            
            if 'Destination' not in df_housing.columns:
                print(f"File: {file} | Column 'Destination' not found.")
                continue
            
            # Count only specific permanent housing values
            permanent_housing_mask = df_housing['Destination'].isin(permanent_housing_values)
            num_permanent_housing = permanent_housing_mask.sum()
            
            # Extract program ID from filename (assuming it's at the beginning)
            program_id = file.split(' ')[0]
            
            # Print results for this file
            print(f"Program: {program_id} | Total clients: {total_clients} | Exited to permanent housing: {num_permanent_housing}")
        
        except Exception as e:
            print(f"Error processing {file}: {e}")

# %%
# Define permanent housing values to count
permanent_housing_values = [
    'Rental by client, with ongoing housing subsidy (HUD)',
    'Rental by client, no ongoing housing subsidy (HUD)',
    'Owned by client, no ongoing housing subsidy (HUD)',
    'Owned by client, with ongoing housing subsidy (HUD)',
    'Long-term care facility or nursing home (HUD)',
    'Staying or living with family, permanent tenure (HUD)',
    'Staying or living with friends, permanent tenure (HUD)'
]

# Create a list to store results
results = []

# Process each file in the folder
for file in os.listdir(folder_path):
    if file == "TEMPLATE RAW Client Data Export v3_EE Workflow.xlsx":
        continue  # Skip this specific file
    
    if file.endswith(".xlsx"):
        file_path = os.path.join(folder_path, file)
        
        try:
            # Load the dataframe for this file
            df_housing = pd.read_excel(file_path, sheet_name="ENTRY-EXIT")
            total_clients = len(df_housing)
            
            # Extract program name from filename (before the word RAW)
            program_parts = file.split('RAW')[0].strip()
            
            if 'Destination' not in df_housing.columns:
                print(f"File: {file} | Column 'Destination' not found.")
                continue
            
            # Count only specific permanent housing values
            permanent_housing_mask = df_housing['Destination'].isin(permanent_housing_values)
            num_permanent_housing = permanent_housing_mask.sum()
            
            # Store results
            results.append({
                'Program': program_parts,
                'Total Clients': total_clients,
                'Permanent Housing Count': num_permanent_housing
            })
            
            print(f"Processed: {file}")
        
        except Exception as e:
            print(f"Error processing {file}: {e}")

# %%
# Create a DataFrame from the results
results_df = pd.DataFrame(results)

# Save to Excel
output_path = os.path.join('BoSClean', "Permanent_Housing_Count.xlsx")
results_df.to_excel(output_path, index=False)

print(f"Results saved to {output_path}")

# %% [markdown]
# ### Breakdown of exit destinations (permanent housing, shelter, streets, etc.)

# %%
# Create a list to store results
destination_counts = []

# Process each file in the folder
for file in os.listdir(folder_path):
    if file == "TEMPLATE RAW Client Data Export v3_EE Workflow.xlsx":
        continue  # Skip this specific file
    
    if file.endswith(".xlsx"):
        file_path = os.path.join(folder_path, file)
        
        try:
            # Load the dataframe for this file
            df_housing = pd.read_excel(file_path, sheet_name="ENTRY-EXIT")
            
            # Extract program ID from filename (before the word RAW)
            program_id = file.split('RAW')[0].strip()
            
            if 'Destination' not in df_housing.columns:
                print(f"File: {file} | Column 'Destination' not found.")
                continue
            
            # Get value counts for all destinations
            counts = df_housing['Destination'].value_counts().reset_index()
            counts.columns = ['Exit Destination', 'Count']
            counts['Program ID'] = program_id
            
            # Reorder columns to match your screenshot
            counts = counts[['Program ID', 'Exit Destination', 'Count']]
            
            # Append all counts for this program to our results
            destination_counts.extend(counts.to_dict('records'))
            
            print(f"Processed: {file}")
        
        except Exception as e:
            print(f"Error processing {file}: {e}")

# %%
# Create a DataFrame from the results
results_df = pd.DataFrame(destination_counts)

# Save to Excel
output_path = os.path.join('BoSClean', "destination_value_counts.xlsx")
results_df.to_excel(output_path, index=False)

print(f"Results saved to {output_path}")

# %%
# Read the original data
input_file = "destination_value_counts.xlsx"

# Load the data
df = pd.read_excel(input_file)

# Get top 3 destinations for each program
top3_df = (df.sort_values(['Program ID', 'Count'], ascending=[True, False])
           .groupby('Program ID')
           .head(3)
           .reset_index(drop=True))

# Pivot the data to have Program ID in one column and destinations in separate columns
final_df = top3_df.assign(rank=top3_df.groupby('Program ID').cumcount()+1) \
                .pivot(index='Program ID', columns='rank') \
                .reset_index()

# Flatten multi-index columns
final_df.columns = ['Program ID'] + \
                 [f'Destination {i}' for i in range(1,4)] + \
                 [f'Count {i}' for i in range(1,4)]

# Save to new Excel file
output_path = os.path.join('BoSClean', "program_top_destinations.xlsx")
final_df.to_excel(output_path, index=False)

# %% [markdown]
# ### Average length of time to housing move-in 

# %%
# Create a list to store results
results = []

# Process each file
for file in os.listdir(folder_path):
    if file == "TEMPLATE RAW Client Data Export v3_EE Workflow.xlsx":
        continue
    
    if file.endswith(".xlsx"):
        file_path = os.path.join(folder_path, file)
        
        try:
            # Load only the ENTRY-EXIT sheet
            df = pd.read_excel(file_path, sheet_name="ENTRY-EXIT")
            
            # Get program ID from filename
            program_id = file.split('RAW')[0].strip()
            
            # Convert dates
            df['Entry Date'] = pd.to_datetime(df['Entry Date'], errors='coerce')
            df['Housing Move-in Date'] = pd.to_datetime(df['Housing Move-in Date(12855)'], errors='coerce')
            
            # Calculate days to move-in
            df['Days_to_MoveIn'] = (df['Housing Move-in Date'] - df['Entry Date']).dt.days
            
            # Filter valid cases (positive days and has move-in date)
            valid_cases = df[
                (df['Days_to_MoveIn'] > 0) & 
                (df['Housing Move-in Date'].notna())
            ]
            
            # Calculate average days for this program
            avg_days = valid_cases['Days_to_MoveIn'].mean()
            
            # Store results for each valid case
            for days in valid_cases['Days_to_MoveIn']:
                results.append({
                    'Program ID': program_id,
                    'Days to Move In': days,
                    'Average Days to Move In': avg_days
                })
            
            print(f"Processed {file}: {len(valid_cases)} valid cases")
            
        except Exception as e:
            print(f"Error processing {file}: {e}")

# %%
if results:
    results_df = pd.DataFrame(results)

# Save to Excel
output_path = os.path.join('BoSClean', "days_to_movein_filtered.xlsx")
results_df.to_excel(output_path, index=False)

print(f"Results saved to {output_path}")


