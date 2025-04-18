#  Adds a UID column to the DataFrame by joining 'Provider Tree' and 'Provider Abbrev' with a hyphen.
# Example: 143 and ORRH2 → 143-ORRH2
def add_uid_column(df):
    if 'Provider Tree' in df.columns and 'Provider Abbrev' in df.columns:
        df['UID'] = df['Provider Tree'].astype(str) + "-" + df['Provider Abbrev'].astype(str)
    else:
        print("⚠️ Warning: 'Provider Tree' or 'Provider Abbrev' column not found in the DataFrame.")
    return df
