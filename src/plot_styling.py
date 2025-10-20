
def fontsize_style() -> dict[str, str]:
    """Dict with fontsize and fontweight options: meant to be unpacken in plt call.

    Returns:
        dict[str, str]:
    """
    fontsize = {"fontsize": "22", "fontweight": "bold"}

    return fontsize


def line_style() -> dict[str, str]:
    """The thickness and color of the plotted line. Unpack in plt call.

    Returns:
        dict[str, str]:
    """
    linestyle = {"linewidth": 4, "c": "#90ff63"}

    return linestyle
