import pandas as pd

# percent ice runoff versus surface discharge (see Miaja's COLAB)

# I am purple (SW)
# RACMO: runoff, temperature, precipitation; GRACE: mass balance; Mankoff: ice discharge

# grace = following data minus the previous year 
# calculated mass balance - grace , summed by year (group by year. sum())
# calculated mass balance = 

def _import_file(filename: str, date_format: str, **kwargs) -> pd.DataFrame:
    """Import one of the data files - to be used for grace and ice discharge because those dfs don't have two date columns (Year and Month)

    Args:
        filename (str):

    Returns:
        pd.DataFrame:
    """
    df = pd.read_csv(
        f"/home/achen7/icy/data/{filename}",
        delimiter=",",
        date_format=date_format,
        na_values=["NaN", "NAN", "NaN", "None", "nan", "99999.9"],
        **kwargs,
    )

    return df


def _format_date(df: pd.DataFrame) -> pd.DataFrame:
    """Format an 'Year' and 'Month' column into a new column named to 'Date_new' where the datetime format is ex) 2002-04-01, so %Y-%m-%d

    Args:
        df (pd.DataFrame):

    Returns:
        pd.DataFrame:
    """
    df["Date_new"] = pd.to_datetime(df[["Year", "Month"]].assign(DAY=1))

    return df


def _smol_df(df: pd.DataFrame,
                date_column_name: str,
                measurement_column: str,
                renamed_column: str) -> pd.DataFrame:
    """Pull the date and the measurement column only. Then renames the measurement column to something descriptive. Then sets time column as index. Assumes that the date has already been formatted into %Y-%m-%d.

    Args:
        df (pd.DataFrame): Raw df, altered with an additional date column which puts Year and Month column into one date column with %Y-%m-%d format.
        date_column_name (str): The column that is already manipulated into %Y-%m-%d format.
        measurement_column (str): ex) for RACMO dfs- mine is "SW" column
        renamed_column (str): ex) "Date"

    Returns:
        pd.DataFrame:
    """
    df_smol = df[[date_column_name, measurement_column]]
    df_smol = df_smol.rename(columns={measurement_column: renamed_column})
    df_smol.set_index(date_column_name, inplace=True)
    
    return df_smol
    
    
def import_grace_smb() -> pd.DataFrame:
    """Changes the original Year-Month date format into a 'Date' column in %Y-%m-%d format and sets that as the time index. Other column is 'sw_grace_gt_month'

    Returns:
        pd.DataFrame:
    """
    mass_balance_df = _import_file(
        filename="averaged_GRACE_GMB_basin_gigatons_month_mass_balance.csv",
        date_format="%Y-%b",
        parse_dates=[" - Year-Month"],
    )

    # Create an Year column and a Month column
    mass_balance_df["Year"] = mass_balance_df[" - Year-Month"].dt.year
    mass_balance_df["Month"] = mass_balance_df[" - Year-Month"].dt.month
    # Create final time column in %Y-%m-%d format
    mass_balance_df = _format_date(df=mass_balance_df)
    # Drop the previous - Year-month column and extra created Year and Month columns
    mass_balance_df = mass_balance_df.drop(" - Year-Month", axis=1)
    mass_balance_df = mass_balance_df.drop("Year", axis=1)
    mass_balance_df = mass_balance_df.drop("Month", axis=1)

    grace_df = _smol_df(
        df=mass_balance_df,
        date_column_name="Date_new",
        measurement_column="AVERAGE of SW",
        renamed_column="sw_grace_gt_month",
    )
    
    # subtract the following value from next row from the current value
    grace_df["sw_grace_diff_gt_month"] = grace_df.diff()

    return grace_df


# Plot data 2009-2018 cause that's where the other basins have all data
def import_mankoff_ice_discharge() -> pd.DataFrame:
    """Creates mini df with 'Date' column set as index in %Y-%m-%d format and other column is "sw_avg_ice_disch_gt_month"

    Returns:
        pd.DataFrame:
    """
    ice_discharge_df = _import_file(
        filename="Mankoff_region_D_Gt_month-1_ice_discharge_avg.csv",
        date_format="%m/%d/%y",
        parse_dates=["Date"],
    )

    # Convert original Date column to datetime time cause it is object type rn for some reason
    ice_discharge_df["Date"] = pd.to_datetime(ice_discharge_df["Date"])

    ice_discharge_df_mini = _smol_df(df=ice_discharge_df,
                                     date_column_name="Date",
                                     measurement_column="SW",
                                     renamed_column="sw_avg_ice_disch_gt_month")

    return ice_discharge_df_mini


def import_runoff() -> pd.DataFrame:
    """SW runoff gt/month, "Date" and "sw_runoff_gt_month" columns. Dates formatted %Y-%m-%d.

    Returns:
        pd.DataFrame:
    """
    runoff_df = _import_file(
        filename="RACMO_runoff_gigatons_per_month.csv",
        date_format="%Y",
    )

    runoff_df = _format_date(df=runoff_df)
    
    runoff_df_mini = _smol_df(df=runoff_df,
                              date_column_name="Date_new",
                              measurement_column="SW",
                              renamed_column="sw_runoff_gt_month")
    
    return runoff_df_mini


def import_ppt() -> pd.DataFrame:
    """SW sum ppt in gigatons for each month, "Date" and "sw_sum_ppt_gt_each_month" columns. Dates formatted %Y-%m-%d.

    Returns:
        pd.DataFrame: 
    """
    ppt_df = _import_file(
        filename="RACMOdataset_monthly_PRECIP_sum_(Gt).csv",
        date_format="%Y"
    )
    
    ppt_df = _format_date(df=ppt_df)
    ppt_df_mini = _smol_df(
        df=ppt_df,
        date_column_name="Date_new",
        measurement_column="SW",
        renamed_column="sw_sum_ppt_gt_each_month",
    )

    return ppt_df_mini


def import_temp_2m() -> pd.DataFrame:
    """SW avg air temp 2m above surface in K for each month. "Date" and "sw_monthly_avg_temp_2m" columns. Dates formatted %Y-%m-%d.

    Returns:
        pd.DataFrame:
    """
    temp_df = _import_file(
        filename="RACMOdataset_monthly_T(air 2m above surface)_avg_(K).csv",
        date_format="%Y"
    )
    
    temp_df = _format_date(df=temp_df)
    temp_df_mini = _smol_df(
        df=temp_df,
        date_column_name="Date_new",
        measurement_column="SW",
        renamed_column="sw_monthly_avg_temp_2m_K",
    )

    return temp_df_mini
    

def concat_dfs() -> pd.DataFrame:
    """Imports all dfs and drops the nans, as to which pd.concat works.

    Returns:
        pd.DataFrame: Concatted df with all current columns ['sw_grace_gt_month', 'sw_avg_ice_disch_gt_month', 'sw_runoff_gt_month',
       'sw_sum_ppt_gt_each_month', 'sw_monthly_avg_temp_2m_K']
    """
    mass_balance_df = import_grace_smb()
    ice_discharge_df = import_mankoff_ice_discharge()
    runoff_df = import_runoff()
    ppt_df = import_ppt()
    temp_df = import_temp_2m()
    
    dfs = {
        "mass_balance": mass_balance_df,
        "ice": ice_discharge_df,
        "runoff": runoff_df,
        "ppt": ppt_df,
        "temp": temp_df
    }
    for key, df in dfs.items():
        dfs[key] = df.dropna()  # Drop nans in each df


    concat_df = pd.concat(dfs.values(), axis=1)
    
    print("NaT count in final index:", concat_df.index.isna().sum())
    print("Is index monotonic?", concat_df.index.is_monotonic_increasing)
    print("Index dtype:", concat_df.index.dtype)

    return concat_df
    

    # # Drop duplicate indices from each DataFrame
    # for name, df in dfs.items():
    #     if not df.index.is_unique:
    #         dup_count = df.index.duplicated().sum()
    #         print(f"{name}: {dup_count} duplicate index values removed")
    #         dfs[name] = df[~df.index.duplicated(keep="first")]

    # concat_df = pd.concat(dfs.values(), axis=1)
    
    # # Remove NaTs
    # concat_df = concat_df[~concat_df.index.isna()]

    # # Make time monotonic 
    # concat_df = concat_df.sort_index()
    


def slice_big_df() -> pd.DataFrame:
    """Slice to 2009-2018 period.

    Returns:
        pd.DataFrame:
    """
    sliced_df = concat_dfs().loc["2009-01-01":"2018-12-31"]

    return sliced_df


def main():
    concat_df = concat_dfs()
    #print(concat_df)


if __name__ == "__main__":
    main()


# 10-21 findings
# ice discharge df has duplicate index values 
# DatetimeIndex(['2000-09-01', '2007-09-01', '2008-06-01', '2008-08-01',
#                '2008-09-01', '2008-11-01', '2009-01-01', '2009-02-01',
#                '2009-03-01', '2009-04-01',
#                ...
#                '2024-11-01', '2024-12-01', '2025-01-01', '2025-02-01',
#                '2025-03-01', '2025-04-01', '2025-05-01', '2025-06-01',
#                '2025-07-01', '2025-08-01'],
#               dtype='datetime64[ns]', name='Date', length=204, freq=None)


# grace:
#  index dtype: <class 'pandas.core.indexes.datetimes.DatetimeIndex'> datetime64[ns]
#  index is DatetimeIndex? True
#  min, max: 2002-04-01 00:00:00 2024-05-01 00:00:00
#  length: 230
#  num NaT in index: 0
#  num duplicate index values: 0
# DatetimeIndex(['2002-04-01', '2002-05-01', '2002-08-01', '2002-09-01',
#                '2002-10-01'],
#               dtype='datetime64[ns]', name='Date_new', freq=None)

# ice:
#  index dtype: <class 'pandas.core.indexes.datetimes.DatetimeIndex'> datetime64[ns]
#  index is DatetimeIndex? True
#  min, max: 1986-04-15 00:00:00 2025-08-20 00:00:00
#  length: 3426
#  num NaT in index: 501
#  num duplicate index values: 500
# DatetimeIndex(['1986-04-15', '1986-05-15', '1986-06-15', '1986-07-15',
#                '1986-08-15'],
#               dtype='datetime64[ns]', name='Date', freq=None)

# runoff:
#  index dtype: <class 'pandas.core.indexes.datetimes.DatetimeIndex'> datetime64[ns]
#  index is DatetimeIndex? True
#  min, max: 2000-09-01 00:00:00 2018-12-01 00:00:00
#  length: 999
#  num NaT in index: 779
#  num duplicate index values: 778
# DatetimeIndex(['2000-09-01', '2000-10-01', '2000-11-01', '2000-12-01',
#                '2001-01-01'],
#               dtype='datetime64[ns]', name='Date_new', freq=None)

# ppt:
#  index dtype: <class 'pandas.core.indexes.datetimes.DatetimeIndex'> datetime64[ns]
#  index is DatetimeIndex? True
#  min, max: 2000-09-01 00:00:00 2018-12-01 00:00:00
#  length: 220
#  num NaT in index: 0
#  num duplicate index values: 0
# DatetimeIndex(['2000-09-01', '2000-10-01', '2000-11-01', '2000-12-01',
#                '2001-01-01'],
#               dtype='datetime64[ns]', name='Date_new', freq=None)

# temp:
#  index dtype: <class 'pandas.core.indexes.datetimes.DatetimeIndex'> datetime64[ns]
#  index is DatetimeIndex? True
#  min, max: 2000-09-01 00:00:00 2018-12-01 00:00:00
#  length: 220
#  num NaT in index: 0
#  num duplicate index values: 0
# DatetimeIndex(['2000-09-01', '2000-10-01', '2000-11-01', '2000-12-01',
#                '2001-01-01'],
#               dtype='datetime64[ns]', name='Date_new', freq=None)