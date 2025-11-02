import pandas as pd
import matplotlib.pyplot as plt

from create_big_df import import_file

from plot_styling import fontsize_style
from splots.saxes import thic_plot


def _import_total_loss() -> pd.DataFrame:
    """Imports total loss df (total loss = runoff + ice discharge, so units are Gt/month) and sets "Date" column as index.

    Returns:
        pd.DataFrame:
    """
    total_loss_df = import_file(
        filename="Final_Plots_Datasets - Total_loss (not normalized; runoff + ice discharge.csv",
        date_format="%m/%d/%Y",
        parse_dates=["Date"],
    )

    # Drop Month and Year columns
    total_loss_df = total_loss_df.drop(["Year", "Month"], axis=1)

    total_loss_df = total_loss_df.set_index("Date")

    return total_loss_df


def plot_total_loss():
    plt.style.use("dark_background")

    total_loss_df = _import_total_loss()

    fontstyle = fontsize_style()

    # Col map with color
    region_color = {
        "SE": "#f23f5d",
        "E+W": "#4bf288",
        "N+NW": "#4fadff",
        "NE": "#ffbe0d",
        "SW": "#afa1ff",
    }
    # Area of each basin- normalize total loss by area of each region 
    region_area = {
        "SE": 165348.6113,
        "E+W": 662182.9852,
        "N+NW": 547172.7864,
        "NE": 425242.1042,
        "SW": 216207.285
    }

    fig, ax = plt.subplots(nrows=1, ncols=1)

    for col, pnt_color in region_color.items():
        ax.scatter(
            total_loss_df.index,
            total_loss_df[col]
            / region_area[
                col
            ] * 10**3,  # Normalize total loss by area to make values more comparable and make Gt into Mt 
            s=200,
            edgecolor="white",
            linewidth=0.01,
            c=pnt_color,
            label=col,
        )
    legend = ax.legend(fontsize=15)
    
    ax.set_ylabel("Total Loss GrIS / (Mt $\\cdot$ month$^{-1} \\cdot km^{2}$))", **fontstyle)
    ax.set_xlabel("Datetime", **fontstyle)
    thic_plot(ax)

    plt.show()


def main():
    plot_total_loss()
    

if __name__ == "__main__":
    main()
