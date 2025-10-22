
from typing import Any 

def fontsize_style() -> dict[str, Any]:  # used Any instead of str to avoid error in script...
    """Dict with fontsize and fontweight options: meant to be unpacken in plt call.

    Returns:
        dict[str, str]:
    """
    fontsize = {"fontsize": "22", "fontweight": "bold"}

    return fontsize


def scatter_style() -> dict[str, float | str]:
    """Unpack in plt.scatter() - stylizes scatter points

    Returns:
        dict[str, float | str]:
    """
    style = {
        "s": 100,
        "edgecolor": "#d90b0b",
        "linewidth": 0.05,
        "c": "#90ff63",
        "alpha": 0.8
    }
    return style
