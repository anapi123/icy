import pandas as pd
from create_big_df import import_file


def import_final_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Imports final data files and sets date column as index.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: 
    """
    date_format = "%m/%d/%Y"
    parse_dates = "Date"

    total_loss = import_file(
        filename="final_data/Final_Plots_Datasets - Total_loss (not normalized; runoff + ice discharge.csv",
        date_format=date_format,
        parse_dates=[parse_dates],
    )

    t_2m = import_file(
        filename="final_data/Final_Plots_Datasets - T2m(avg,K).csv",
        date_format=date_format,
        parse_dates=[parse_dates],
    )

    grace_diffs = import_file(
        filename="final_data/Final_Plots_Datasets - GRACE_diffs ((P-R-ID)-Grace diff).csv",
        date_format=date_format,
        parse_dates=[parse_dates],
    )

    for df in [total_loss, t_2m, grace_diffs]:
        df.set_index("Date", inplace=True)

    return total_loss, t_2m, grace_diffs


def write_stats_output():
    """Writes the df.describe() output to csv which is rounded to 2 decimal places.
    """
    total_loss, t_2m, grace_diffs = import_final_data()
    df_name = {"total_loss": total_loss,
               "t_2m": t_2m, 
               "grace_diffs": grace_diffs}
    
    for name, df in df_name.items():
        filepath = f"/home/achen7/icy/data/{name}_pd_describe.csv"
        stats_df = df.describe()
        rounded_df = stats_df.round(2)
        rounded_df.to_csv(filepath, sep=",")
        print(f"{name} df written to csv")


def main():
    write_stats_output()

if __name__ == "__main__":
    main()
