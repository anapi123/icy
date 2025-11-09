import pandas as pd
import matplotlib.pyplot as plt

from create_big_df import import_file
from plot_styling import fontsize_style, line_style

from splots.saxes import thic_plot


def get_sw_file() -> pd.DataFrame:
    """Returns my SW data file with columns

    ['sw_grace_gt_month', 'sw_grace_diff_gt_month',
    'sw_avg_ice_disch_gt_month', 'sw_runoff_gt_month',
    'sw_sum_ppt_gt_each_month', 'sw_monthly_avg_temp_2m_K',
    'sw_total_ice_loss_gt_month', 'sw_ice_discharge_percent',
    'sw_grace_diffs_gt_month']

       and time index set.

    Returns:
        pd.DataFrame:
    """
    sw = import_file(
        filename="new_sw_monthly_resampled.csv",
        date_format="%Y-%m-%d",
        parse_dates=["Date"],
    )

    sw.set_index("Date", inplace=True)

    return sw


def mass_loss_barplot() -> None:
    """Plots yearly sum of ID and R that is color coded
    """
    fontstyle = fontsize_style()

    sw = get_sw_file()
    barplot_df = sw[
        [
            "sw_avg_ice_disch_gt_month",
            "sw_runoff_gt_month",
        ]
    ]

    # Want the annual ice discharge and runoff so sum instead of average
    barplot_df = barplot_df.resample("YE").sum()
    # Rename columns for legend
    barplot_df = barplot_df.rename(
        columns={
            "sw_avg_ice_disch_gt_month": "Ice discharge",
            "sw_runoff_gt_month": "Runoff",
        }
    )
    # All the dates said 1970 if this was not done
    barplot_df.index = barplot_df.index.year.astype(str)

    ax = barplot_df.plot(
        kind="bar",
        stacked=True,
        color={"Ice discharge": "#fdb950", "Runoff": "#8d5fa8"},
        width=0.9
    )

    ax.set_ylabel("SW Annual Sum Total Loss / (Gt $\\cdot$ yr$^{{-1}}$)", **fontstyle)
    ax.set_xlabel("Year", **fontstyle)

    ax.legend(frameon=False, fontsize=22)
    thic_plot(ax)

    plt.show()

def ice_discharge_runoff() -> None:
    """Plots ID and R in subplot line form
    """
    fontstyle = fontsize_style()
    linestyle = line_style()

    sw = get_sw_file()
    
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)
    
    x_time = sw.index
    # ice discharge
    ax1.plot(x_time, sw["sw_avg_ice_disch_gt_month"], **linestyle)
    ax1.set_ylabel("SW Avg Ice Discharge /\n(Gt $\\cdot$ month$^{{-1}}$)", **fontstyle)
    # runoff
    ax2.plot(x_time, sw["sw_runoff_gt_month"], **linestyle)
    ax2.set_ylabel("SW Runoff /\n(Gt $\\cdot$ month$^{{-1}}$)", **fontstyle)
    ax2.set_xlabel("Date", **fontstyle)
    
    for ax in [ax1, ax2]:
        thic_plot(ax)
    
    plt.show()

def pred_mb() -> None:
    """Plots P - R - D- aka predicted MB 
    """
    fontstyle = fontsize_style()
    linestyle = line_style()

    sw = get_sw_file()
    
    fig, ax = plt.subplots()
    
    # Calculate p - r - d
    y_pred_mb = (
        sw["sw_sum_ppt_gt_each_month"]
        - sw["sw_runoff_gt_month"]
        - sw["sw_avg_ice_disch_gt_month"]
    )
    
    ax.plot(sw.index, y_pred_mb, **linestyle)
    ax.set_ylabel("SW Predicted MB ≝ (P - R - ID)/ (Gt $\\cdot$ month$^{{-1}}$)", **fontstyle)
    ax.set_xlabel("Date", **fontstyle)
    thic_plot(ax)
    
    plt.show()
    

def main():
    #pred_mb()
    pd.set_option("display.max_columns", None)

    df = get_sw_file()
    describe_df = df.describe()
    print(describe_df.loc[["min", "max"]])

if __name__ == "__main__":
    main()
