import pandas as pd 

# todo get 1) temperature data in RACMO and 2) precip data in RACMO 
# percent ice runoff versus surface discharge (see Miaja's COLAB)

# RACMO: runoff, temperature, precipitation; GRACE: mass balance; Mankoff: ice discharge 



def _import_file(filename: str, 
                 date_format: str, 
                 time_column_name: str) -> pd.DataFrame:
    """Import one of the data files.

    Args:
        filename (str):
        date_format (str):
        time_column_name (str):

    Returns:
        pd.DataFrame: 
    """
    df = pd.read_csv(
        f"/home/achen7/icy/data/{filename}",
        delimiter=",",
        na_values=["NaN", "NAN", "NaN", "None", "nan", "99999.9"],
        date_format=date_format,
        parse_dates=[time_column_name],
    )
    
    return df

def import_grace_smb():
    mass_balance_df = _import_file(
        filename="averaged_GRACE_GMB_basin_gigatons_month_mass_balance.csv",
        date_format="%Y-%b",
        time_column_name=" - Year-Month",
    )
    
    return mass_balance_df

def import_mankoff_ice_discharge():
    ice_discharge_df = _import_file(
        filename="Mankoff_region_D_Gt_month-1_ice_discharge_avg.csv",
        date_format="%m/%d/%y",
        time_column_name="Date",
    )
    
    return ice_discharge_df

def import_runoff():
    runoff_df = _import_file(
        filename="RACMO_runoff_gigatons_per_month.csv",
        date_format="%Y",
        time_column_name="Year",
    )
    
    return runoff_df

def main():
    mass_balance_df = import_grace_smb()
    ice_discharge_df = import_mankoff_ice_discharge()
    runoff_df = import_runoff()
    
    for df in [mass_balance_df, ice_discharge_df, runoff_df]:
        print(df)
        print("###############")

if __name__ == "__main__":
    main()