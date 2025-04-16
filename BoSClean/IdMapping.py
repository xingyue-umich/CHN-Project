import pandas as pd

# Maps an EE Provider ID to an acronym.
# Returns None if the ID should be skipped.
def get_provider_info(ee_provider_id):

    # The Provider Ids we want to exclude
    exclude_ids = {"Community Housing Network – Oakland County – Housing Stability Services(13481)",
                "XXXCLOSED 2024 - Community Housing Network - Macomb Co. - MSHDA ESG FY22 - Prevention(13571)",
                "Community Housing Network - Oakland County - MSDHA HOME-ARP: Oakland HCV Mobility Program(13783)",
                "Community Housing Network - Oakland County - MSDHA HOME-ARP: Housing Navigation Program (HNP)(13639)",
                "Community Housing Network - Oakland County - Housing for Older Persons (HOP) HNP(13700)",
                "XXXCLOSED2023 - Oakland County - Community Housing Network - CHID ESG Prevention (HPRP)(12114)",
                "Community Housing Network - Macomb County - MSDHA HOME-ARP: Macomb HCV Mobility Program(13790)"}  

    if ee_provider_id in exclude_ids:
        return None


    # Map provider id to abbreviation and program tree
    # {Provider id : {abbrev}}
    provider_info = {
        "Community Housing Network, Inc. - Macomb Co. - Macomb Leasing Assistance Program 7(9643)": {
            "abbrev": "MLAP7",
            "tree": "1371"
        },

        "Community Housing Network, Inc. - Out Wayne - Chronically Homeless Leasing Assistance Program 1(11496)" : {
            "abbrev": "WCHLAP1",
            "tree": "11495"
        },
        
        "Community Housing Network, Inc. - Oakland County - Leasing Assistance Program (CG)(9182)" : {
            "abbrev": "OLAP CG",
            "tree": "143"        
        },
        
        "Community Housing Network, Inc. - Oakland County - Chronically Homeless Leasing Assistance 2(3030)" : {
            "abbrev": "OCHLAP2",
            "tree": "143"                
        },
        
        "Community Housing Network, Inc. - Macomb Co. - Macomb Leasing Assistance Program 1(1372)" : {
            "abbrev": "MLAP1",
            "tree": "1371"            
        },
        
        "MDHHS - Community Housing Network, Inc. - Oakland CoC - Shelter Plus Care Program(3056)" : {
            "abbrev": "SPC",
            "tree": "3055"             
        },
        
        "Community Housing Network, Inc. - Macomb CoC -  RRH - MSHDA ESG(14415)" : {
            "abbrev": "MC RRH",
            "tree": "1371"             
        },
        
        "Community Housing Network - Oakland County - Rapid Rehousing Program2 (ORRH2)(11038)" : {
            "abbrev": "ORRH2",
            "tree": "143"             
        },
        
        "Community Housing Network, Inc. - Jefferson Oaks SHU Oakland County(11485)" : {
            "abbrev": "Jefferson Oaks SHU",
            "tree": "143"             
        },
               
        "MDHHS - Community Housing Network - Oakland CoC - PATH - Services Only(10545)" : {
            "abbrev": "OC PATH",
            "tree": "1492"            
        },
        
        "Community Housing Network, Inc. - Palmer Pointe SHU Oakland County(9249)" : {
            "abbrev": "Palmer Pointe SHU",
            "tree": "143"            
        },
        
        "HARA - Oakland County - Community Housing Network - MSDHA ESG 2016-Present - RRH(10989)" : {
            "abbrev": "ORRH",
            "tree": "8319"             
        },
        
        "HARA - Oakland County - Community Housing Network - MSDHA ESG 2016-Present - Prevention(10988)" : {
            "abbrev": "Prevention",
            "tree": "8319"             
        },
        
        "Community Housing Network, Inc. - Oakland County - Leasing Assistance Program 2(281)" : {
            "abbrev": "OLAP2",
            "tree": "143"              
        },
        
        "Community Housing Network, Inc. – Erin Park SHU – Macomb CoC(12859)" : {
            "abbrev": "Erin Park SHU",
            "tree": "12312"            
        },
        
        "XXXCLOSED2024 - Community Housing Network, Inc. - Macomb Co. - Macomb Leasing Assistance Program 2(3032)" : {
            "abbrev": "MLAP2",
            "tree": "1371" 
        },
        
        "Community Housing Network, Inc. - Oakland County - Chronically Homeless Leasing Assistance 1(1130)" : {
            "abbrev": "OCHLAP1",
            "tree": "143"             
        },
        
        "MDHHS - Community Housing Network - Oakland CoC - PATH Outreach Only(1493)" : {
            "abbrev": "OC PATH",
            "tree": "1492"              
        },
        
        "MDHHS - Community Housing Network - Macomb CoC - PATH Outreach Only(11690)" : {
            "abbrev": "MC PATH",
            "tree": "1492"              
        },
        
        "MDHHS - Community Housing Network - Macomb CoC - PATH - Services Only(11694)" : {
            "abbrev": "MC PATH",
            "tree": "1492"              
        },
        
        "Community Housing Network, Inc. - Macomb Co. - Chronically Homeless Leasing Assistance 1 (HUD)(3033)" : {
            "abbrev": "MCHLAP1",
            "tree": "1371"             
        },
        
        "Community Housing Network, Inc. - Macomb Co. - Chronically Homeless Leasing Assistance 6(11031)" : {
            "abbrev": "MCHLAP6",
            "tree": "1371"              
        },
        
        "Community Housing Network, Inc. - Grafton SHU Oakland County (Macomb)(10824)" : {
            "abbrev": "Grafton SHU",
            "tree": "143"             
        },
        
        "Community Housing Network, Inc. - Macomb Co. - Chronically Homeless Leasing Assistance 5(10327)" : {
            "abbrev": "MCHLAP5",
            "tree": "1371"             
        },
        
        "Community Housing Network, Inc. - Unity Park SHU Oakland County - All Phases(10170)" : {
            "abbrev": "Unity Park SHU",
            "tree": "143"             
        },
        
        "Community Housing Network, Inc. - Macomb Co. - Macomb Leasing Assistance Program 6(8964)" : {
            "abbrev": "MLAP6",
            "tree": "1371"             
        },
        
        "Community Housing Network - Oakland County - Rapid Rehousing Program(10312)" : {
            "abbrev": "ORRH",
            "tree": "143"             
        },
        
        "Community Housing Network, Inc. Macomb CoC - Prescreening and Referrals(13082)" : {
            "abbrev": "MC SSO",
            "tree": "1371"             
        },
        
        "Community Housing Network, Inc. - Oakland County - Chronically Homeless Leasing Assistance 5(10646)" : {
            "abbrev": "OCHLAP5",
            "tree": "143"                
        }
    }

    # Look up the value for ee_provider_id in the provider_info dictionary. 
    # If it's not found, return None by default.
    return provider_info.get(ee_provider_id, None)

# Cleans a DataFrame by mapping 'EE Provider ID' to abbreviatiobs and filtering out skipped ones.
# Returns a new DataFrame with a column 'Provider Abbrev'.
def clean_provider_ids(df):

    if "EE Provider ID" not in df.columns:
        print("Column 'EE Provider ID' not found.")
        return df

    # Apply the mapping function
    df["provider_info"] = df["EE Provider ID"].apply(get_provider_info)
    df_cleaned = df[df["provider_info"].notna()].copy()

    # Split the provider_info dictionary into two new columns
    df_cleaned["Provider Abbrev"] = df_cleaned["provider_info"].apply(lambda x: x["abbrev"])
    df_cleaned["Provider Tree"] = df_cleaned["provider_info"].apply(lambda x: x["tree"])

    # Drop the helper column
    df_cleaned.drop(columns=["provider_info"], inplace=True)

    return df_cleaned
