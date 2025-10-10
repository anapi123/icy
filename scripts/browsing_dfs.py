import pandas as pd 

# todo get 1) temperature data in RACMO and 2) precip data in RACMO 
# percent ice runoff versus surface discharge (see Miaja's COLAB)

# I am purple (SW)
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

def _format_date(df: pd.DataFrame,
                 date_column_name: str) -> pd.DataFrame:
    """Format an 'Year' and 'Month' column into a new column named to ex) 'Date' where the datetime format is ex) 2002-04-01, so %Y-%m-%d

    Args:
        df (pd.DataFrame): 
        date_column_name (str): 

    Returns:
        pd.DataFrame: 
    """
    df[date_column_name] = pd.to_datetime(df[["Year", "Month"]].assign(DAY=1))
    
    return df
    
def import_grace_smb() -> pd.DataFrame:
    """Changes the original Year-Month date format into a 'Date' column in %Y-%m-%d format and sets that as the time index. Other column is 'grace_gt_month'

    Returns:
        pd.DataFrame:
    """
    mass_balance_df = _import_file(
        filename="averaged_GRACE_GMB_basin_gigatons_month_mass_balance.csv",
        date_format="%Y-%b",
        time_column_name=" - Year-Month",
    )
    
    # Create an Year column and a Month column 
    mass_balance_df["Year"] = mass_balance_df[" - Year-Month"].dt.year
    mass_balance_df["Month"] = mass_balance_df[" - Year-Month"].dt.month
    # Create final time column in %Y-%m-%d format 
    mass_balance_df["Date"] = pd.to_datetime(mass_balance_df[["Year", "Month"]].assign(DAY=1))
    # Drop the previous - Year-month column and extra created Year and Month columns
    mass_balance_df = mass_balance_df.drop(" - Year-Month", axis=1)
    mass_balance_df = mass_balance_df.drop("Year", axis=1)
    mass_balance_df = mass_balance_df.drop("Month", axis=1)
    
    # Extract final date and my sw column into mini df and rename that sw column
    grace_df = mass_balance_df[["Date", "AVERAGE of SW"]]
    grace_df = grace_df.rename(columns={"AVERAGE of SW": "grace_gt_month"})
    # Set date column as index
    grace_df.set_index("Date", inplace=True)
    
    return grace_df

def import_mankoff_ice_discharge() -> pd.DataFrame:
    """Creates mini df with 'Date' column set as index in %Y-%m-%d format and other column is 'ice_discharge_gt_month'

    Returns:
        pd.DataFrame: 
    """
    ice_discharge_df = _import_file(
        filename="Mankoff_region_D_Gt_month-1_ice_discharge_avg.csv",
        date_format="%m/%d/%y",
        time_column_name="Date",
    )
    
    # Convert original Date column to datetime time cause it is object type rn for some reason 
    ice_discharge_df["Date"] = pd.to_datetime(ice_discharge_df["Date"])
    
    # Extract date and 'AVERAGE OF SW' column
    ice_discharge_df_mini = ice_discharge_df[["Date", "SW"]]
    # Rename average of sw column 
    ice_discharge_df_mini = ice_discharge_df_mini.rename(columns={"SW" : "ice_discharge_gt_month"})    
    # Set Date column as time index
    ice_discharge_df_mini.set_index("Date", inplace=True)
    
    return ice_discharge_df_mini

def import_runoff()-> pd.DataFrame:
    runoff_df = _import_file(
        filename="RACMO_runoff_gigatons_per_month.csv",
        date_format="%Y",
        time_column_name="Year",
    )
    # Format 
    
    return runoff_df

def import_ppt() -> pd.DataFrame:
    ppt_df = _import_file(
        filename="RACMOdataset_monthly_PRECIP_sum_(Gt).csv",
        date_format="%Y",
        time_column_name="Year",
    )

    return ppt_df

def import_temp_2m() -> pd.DataFrame:
    temp_df = _import_file(
        filename="RACMOdataset_monthly_T(air 2m above surface)_avg_(K).csv",
        date_format="%Y",
        time_column_name="Year",
    )

    return temp_df

def main():
    mass_balance_df = import_grace_smb()
    ice_discharge_df = import_mankoff_ice_discharge()
    runoff_df = import_runoff()
    ppt_df = import_ppt()
    temp_df = import_temp_2m()
    
    print(ice_discharge_df)

if __name__ == "__main__":
    main()