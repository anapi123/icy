
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
    style = {"s": 100, "edgecolor": "white", "linewidth": 0.01, "c": "#ffa95e"}
    return style
