"""Figure reading (Nano Omni): axis range, series, values with a stated reading error."""

from __future__ import annotations

import base64

from pydantic import BaseModel, Field

from gapfinder.ingest.pdf import FigureCrop
from gapfinder.models.router import Router


class SeriesPoint(BaseModel):
    series: str
    x: str = Field(description="x category or value as labelled")
    y: float


class FigureReading(BaseModel):
    label: str
    x_axis: str
    y_axis: str
    y_min: float
    y_max: float
    log_scale: bool = False
    points: list[SeriesPoint]
    reading_error: float = Field(description="Estimated absolute error of each y value, in axis units")


FIGURE_PROMPT = """Read the values off this chart from a research paper ({label}).
Caption: {caption}
Report the axis labels and range, every series and every plotted point (bar
heights or line markers), and your reading error in y-axis units. If a panel
has sub-plots, prefix the series name with the panel title."""


async def read_figure(router: Router, fig: FigureCrop) -> FigureReading:
    if fig.png_path is None:
        raise ValueError(f"{fig.label} has no rendered crop")
    b64 = base64.b64encode(fig.png_path.read_bytes()).decode()
    msg = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": FIGURE_PROMPT.format(label=fig.label, caption=fig.caption)},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
            ],
        }
    ]
    reading = await router.structured("omni", msg, FigureReading)
    return reading.model_copy(update={"label": fig.label})


def within_axis_tolerance(read: float, truth: float, y_min: float, y_max: float, frac: float = 0.05) -> bool:
    """M1 eval bar: figure values within 5% of the axis range."""
    return abs(read - truth) <= frac * (y_max - y_min)
