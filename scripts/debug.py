import pandas as pd
import numpy as np
from create_big_df import (
    import_grace_smb,
    import_mankoff_ice_discharge,
    import_ppt,
    import_runoff,
    import_temp_2m,
    concat_dfs
)

def _count_nans(df: pd.DataFrame,
               col_name: str):
    print(f"Column {col_name} has {df[col_name].isna().sum()} nans")

def _slice_df(df: pd.DataFrame) -> pd.DataFrame:
    sliced_df = df.loc["2009-01-01": "2018-12-31"]
    return sliced_df

def grace():
    grace_df = import_grace_smb()
    grace_sliced = _slice_df(grace_df)
    _count_nans(df=grace_sliced, col_name="sw_grace_gt_month")

def ice_disch():
    ice_disch = import_mankoff_ice_discharge()
    ice_sliced = _slice_df(ice_disch)
    _count_nans(df=ice_sliced, col_name="sw_avg_ice_disch_gt_month")

def precip():
    precip = import_ppt()
    precip_sliced = _slice_df(precip)
    _count_nans(df=precip_sliced, col_name="sw_sum_ppt_gt_each_month")

def runoff():
    runoff = import_runoff()
    runoff_sliced = _slice_df(runoff)
    _count_nans(df=runoff_sliced, col_name="sw_runoff_gt_month")

def temp():
    temp = import_temp_2m()
    temp_sliced = _slice_df(temp)
    _count_nans(df=temp_sliced, col_name="sw_monthly_avg_temp_2m_K")

    
    
def print_info_dfs():
    mass_balance_df = import_grace_smb()
    ice_discharge_df = import_mankoff_ice_discharge()
    runoff_df = import_runoff()
    ppt_df = import_ppt()
    temp_df = import_temp_2m()

    # after you import each df (mass_balance_df, ice_discharge_df, etc.)
    for name, df in [
        ("grace", mass_balance_df),
        ("ice", ice_discharge_df),
        ("runoff", runoff_df),
        ("ppt", ppt_df),
        ("temp", temp_df),
    ]:
        print(f"\n{name}:")
        print(" index dtype:", type(df.index), getattr(df.index, "dtype", None))
        print(" index is DatetimeIndex?", isinstance(df.index, pd.DatetimeIndex))
        print(" min, max:", df.index.min(), df.index.max())
        print(" length:", len(df))
        print(" num NaT in index:", df.index.isna().sum())
        print(" num duplicate index values:", df.index.duplicated().sum())
        duplicate_indices = df[df.index.duplicated()]
        print(f"duplicate timestamps: {duplicate_indices}")
        print(df.index[:5])

def print_dfs_duplicates_nats():
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
        "temp": temp_df,
    }

    for name, df in dfs.items():
        # duplicates
        dup_mask = df.index.duplicated(keep="first")
        if dup_mask.any():
            duplicates = df.index[dup_mask]
            print(f"{name}: {len(duplicates)} duplicate timestamps removed:")
            print(duplicates)

        # NaTs
        nat_mask = df.index.isna()
        if nat_mask.any():
            nats = df.index[nat_mask]
            print(f"{name}: {len(nats)} NaT timestamps removed:")
            print(nats)


def main():
    # grace()
    # ice_disch()
    # precip()
    # runoff()
    # temp()
    
    #print_info_dfs()
    print_dfs_duplicates_nats()

if __name__ == "__main__":
    main()
