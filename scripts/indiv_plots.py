import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.axes import Axes

from create_big_df import concat_dfs
from plot_styling import fontsize_style, scatter_style

from splots.saxes import thic_plot


def _create_four_grid() -> list[Axes]:
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, sharex="col")

    axes = [ax1, ax2, ax3, ax4]

    return axes


def _plot_scatter(axes: Axes, 
                  x_series: pd.Series | np.ndarray, 
                  y_series: pd.Series | np.ndarray) -> Axes:
    scatterstyle = scatter_style()
    axes.scatter(x_series, y_series, **scatterstyle)

    return axes


def main():
    
    plt.style.use("dark_background")
    
    #  'sw_avg_ice_disch_gt_month', 'sw_runoff_gt_month', 'sw_sum_ppt_gt_each_month', 'sw_monthly_avg_temp_2m'
    dfs = concat_dfs()
    # ax[0] = ice disch | ax[1] = runoff
    # ax[2] = sum ppt   | ax[3] = avg 2m temp
    axes = _create_four_grid()
    # Import stylization
    fontstyle = fontsize_style()

    # We are looking at 2008-2018 
    df_sliced = dfs.loc["2009-01-01": "2018-12-31"]
    # time
    x_time = df_sliced.index.values
    # shared unit for ice discharge and runoff
    ice_disch_runoff_unit = "(Gt $\\cdot$ month$^{-1}$)"

    ax1 = _plot_scatter(
        axes=axes[0], x_series=x_time, y_series=df_sliced["sw_avg_ice_disch_gt_month"]
    )
    ax1.set_ylabel(f"SW Avg Ice Discharge /\n{ice_disch_runoff_unit}", **fontstyle) 
    
    ax2 = _plot_scatter(axes=axes[1], x_series=x_time, y_series=df_sliced["sw_runoff_gt_month"])
    ax2.set_ylabel(f"SW Runoff /\n{ice_disch_runoff_unit}", **fontstyle) 
    
    ax3 = _plot_scatter(
        axes=axes[2], x_series=x_time, y_series=df_sliced["sw_sum_ppt_gt_each_month"]
    )
    ax3.set_ylabel("SW Monthly\nSum PPT / Gt", **fontstyle)
    
    ax4 = _plot_scatter(
        axes=axes[3], x_series=x_time, y_series=df_sliced["sw_monthly_avg_temp_2m_K"]
    )
    ax4.set_ylabel("SW Monthly Avg\n2m Temp / K", **fontstyle)
    
    # Rotate date ticks 90 degrees for ax3 and ax4
    for ax in [ax3, ax4]:
        ax.tick_params(axis="x", 
                       labelrotation=90)
        for tick in ax.get_xticklabels():
            tick.set_fontweight('bold')
    for ax in axes:
        thic_plot(ax)


    plt.subplots_adjust(left=0.117,
                        bottom=0.126,
                        right=0.983,
                        top=0.98,
                        wspace=0.226,
                        hspace=0.064)
    
    plt.show()

if __name__ == "__main__":
    main()
