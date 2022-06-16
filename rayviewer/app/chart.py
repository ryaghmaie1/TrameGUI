import plotly.graph_objects as go
import pandas as pd

polar_data = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/polar_dataset.csv"
)


def create_polar_fig(width=300, height=300, **kwargs):
    if width < 10:
        width = 10
    if height < 10:
        height = 10

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=polar_data["x1"].tolist(),
            theta=polar_data["y"].tolist(),
            mode="lines",
            name="Figure 8",
            line_color="peru",
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=polar_data["x2"].tolist(),
            theta=polar_data["y"].tolist(),
            mode="lines",
            name="Cardioid",
            line_color="darkviolet",
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=polar_data["x3"].tolist(),
            theta=polar_data["y"].tolist(),
            mode="lines",
            name="Hypercardioid",
            line_color="deepskyblue",
        )
    )

    fig.update_layout(
        # title = 'Mic Patterns',
        margin=dict(l=50, r=50, t=50, b=50),
        showlegend=False,
        width=width,
        height=height,
    )
    return fig
