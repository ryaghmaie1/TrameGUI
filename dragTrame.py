

import plotly.graph_objects as go

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, plotly, html

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
state, ctrl = server.state, server.controller

state.shapes = {}

# -----------------------------------------------------------------------------
# Charts handling
# -----------------------------------------------------------------------------

def create_figure(width=300, height=300, **kwargs):
    figks = go.Figure()

    figks.add_shape(type="circle",
        xref= 'x', yref="y",
        fillcolor='grey',
        x0=-2, y0=-2, x1=2, y1=2,
        line_color='grey',opacity=0.25,
    )
    figks.add_shape(type="circle",
        xref= 'x', yref="y",
        fillcolor="white",
        x0=-1, y0=-1, x1=1, y1=1,
        line_color="white",opacity=0.5,
    )

    figks.update_xaxes(range=[-2, 2], zeroline=False)
    figks.update_yaxes(range=[-2, 2])
    figks.update_layout(width=600, height=600,
                        title = "<b>Plot-1</b>")

    devx = [-0.3, 0.3]
    devy = [-0.2, 0.2]
    figks.add_shape(type="rect",
        xref= 'x', yref="y",
        fillcolor='blue',
        x0=devx[0], y0=devy[0],
        x1=devx[1], y1=devy[1],
        line_color='blue',opacity=0.75, editable=True
    )


    figks.add_shape(type="rect",
        xref= 'x', yref="y",
        fillcolor='red',
        x0=1.2, y0=-1.2,
        x1=1.4, y1=-1.4,
        line_color='red',opacity=0.75, editable=True
    )

    figks.add_shape(type="rect",
        xref= 'x', yref="y",
        fillcolor='green',
        x0=1.5, y0=0,
        x1=1.8, y1=0.3,
        line_color='green',opacity=0.75, editable=True
    )

    return figks


# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------

def on_relayout(event=None):
    print("relayout", event)
    state.shapes = event

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------


state.trame__title = "Charts"

with SinglePageLayout(server) as layout:
    layout.title.set_text("Drag charts")

    with layout.content:
        with vuetify.VContainer(fluid=True, classes="fill-height"):
            with vuetify.VRow():
                with vuetify.VCol():
                    ctrl.update_fig = plotly.Figure(
                        create_figure(),
                        display_mode_bar=("false",),
                        editable=True,
                        edits=("{ shapePosition: true }",),
                        __properties=["edits"],
                        relayout=(on_relayout, "[$event]"),
                    ).update
                with vuetify.VCol():
                    html.Pre("{{ shapes }}")


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()