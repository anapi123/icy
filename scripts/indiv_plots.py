import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes

from create_big_df import concat_dfs
from plot_styling import fontsize_style, line_style

from splots.saxes import thic_plot

def _create_four_grid() -> list[Axes]:
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
    
    axes = [ax1, ax2, ax3, ax4]

    return axes

def _plot_lines(ax: Axes,
                x_series: pd.Series,
                y_series: pd.Series) -> None:
    
    linestyle = line_style()
    ax.plot(x_series, y_series, **linestyle)

def main():
    #  'sw_avg_ice_disch_gt_month', 'sw_runoff_gt_month', 'sw_sum_ppt_gt_each_month', 'sw_monthly_avg_temp_2m'
    dfs = concat_dfs()
    # ax[0] = ice disch | ax[1] = runoff
    # ax[2] = sum ppt   | ax[3] = avg 2m temp
    axes = _create_four_grid()
    # Import stylization 
    fontstyle = fontsize_style()
    
    # time 
    x_time = dfs.index.values 
    
    _plot_lines(ax=axes[0], x_series=x_time, y_series=dfs["sw_avg_ice_disch_gt_month"])
    
    plt.show()
if __name__ == "__main__":
    main()
