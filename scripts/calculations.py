import pandas as pd
from create_big_df import slice_big_df

# try resampling monthly first and then creating new columns

def create_new_cols() -> pd.DataFrame:
    
    df = slice_big_df()
    
    df = df.resample("M").mean()

    # total ice loss = ice discharge + runoff
    df["sw_total_ice_loss_gt_month"] = (
        df["sw_avg_ice_disch_gt_month"] + df["sw_runoff_gt_month"]
    ) * -1  # other ppls values were negative so

    # ice discharge percent = (ice discharge/(ice discharge + runoff))
    df["sw_ice_discharge_percent"] = (
        df["sw_avg_ice_disch_gt_month"]
        / (df["sw_avg_ice_disch_gt_month"] + df["sw_runoff_gt_month"])
        * 100
    )

    # grace dffs = (precip - runoff - ice_disch) - grace diff (subtract the one head from the one before)
    df["sw_grace_diffs_gt_month"] = (
        df["sw_sum_ppt_gt_each_month"]
        - df["sw_runoff_gt_month"]
        - df["sw_avg_ice_disch_gt_month"]
        - df["sw_grace_diff_gt_month"]
    )

    return df


# def resample_sliced_df_monthly() -> pd.DataFrame:
#     """Resample the sliced df with newly added columns, monthly.

#     Returns:
#         pd.DataFrame:
#     """
#     updated_df = _create_new_cols()
#     monthly_df = updated_df.resample("M").mean()
#     return monthly_df

# 10-24 I tried deleting the blanks in runoff and ice discharge near end file (#s appear to match report nats, although that still resulted in nans in the areas seen in final plots spreadsheet. So idk what's going on I think the sw data is just like that)
def write_monthly_csv():
    monthly_df = create_new_cols()
    filepath = "/home/achen7/icy/data/new_sw_monthly_resampled.csv"
    monthly_df.to_csv(filepath, sep=",")
    print(f"{len(monthly_df)} rows written to csv.")
    

def main():
    # df = resample_sliced_df_monthly()
    # print(df)
    write_monthly_csv()


if __name__ == "__main__":
    main()
