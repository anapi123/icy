import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

from create_big_df import import_file
from plot_styling import fontsize_style

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


def mass_loss_barplot():
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
        color={"Ice discharge": "#8d5fa8", "Runoff": "#fdb950"},
    )

    ax.set_ylabel("Annual Sum Total Loss / Gt $\\cdot$ yr$^{{-1}}$", **fontstyle)
    ax.set_xlabel("Year", **fontstyle)

    ax.legend(frameon=False, fontsize=22)
    thic_plot(ax)

    plt.show()


def main():
    mass_loss_barplot()


if __name__ == "__main__":
    main()
