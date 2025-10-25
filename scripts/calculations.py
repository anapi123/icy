import pandas as pd
from create_big_df import concat_dfs


def _slice_big_df() -> pd.DataFrame:
    """Slice to 2009-2018 period.

    Returns:
        pd.DataFrame:
    """
    sliced_df = concat_dfs().loc["2009-01-01":"2018-12-31"]

    return sliced_df


def _create_new_cols() -> pd.DataFrame:
    df = _slice_big_df()

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


def resample_sliced_df_monthly() -> pd.DataFrame:
    """Resample the sliced df with newly added columns, monthly.

    Returns:
        pd.DataFrame:
    """
    updated_df = _create_new_cols()
    monthly_df = updated_df.resample("M").mean()
    return monthly_df

def write_monthly_csv():
    monthly_df = resample_sliced_df_monthly()
    filepath = "/home/achen7/icy/data/sw_monthly_resampled.csv"
    monthly_df.to_csv(filepath, sep=",")
    print(f"{len(monthly_df)} rows written to csv.")
    

def main():
    # df = resample_sliced_df_monthly()
    # print(df)
    write_monthly_csv()


if __name__ == "__main__":
    main()
