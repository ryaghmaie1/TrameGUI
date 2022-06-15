from trame.ui.vuetify import VAppLayout
from trame.widgets import vuetify, vtk, plotly, html

COMPACT_STYLE = dict(dense=True, hide_details=True)


def initialize(server):
    state, ctrl = server.state, server.controller
    state.trame__title = "RayViewer"

    with VAppLayout(server) as layout:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            with vuetify.VCol(cols=4): # Left column
                vuetify.VTextField(
                    label="Variable - 1",
                    v_model=("var_1", "0, 1000, 2000, ..."),
                    **COMPACT_STYLE,
                )
                vuetify.VTextField(
                    label="Variable - 2",
                    v_model=("var_2", "0, 1000, 2000, ..."),
                    **COMPACT_STYLE,
                )
                with vuetify.VRow():
                    with vuetify.VCol(cols=3):
                        vuetify.VSwitch(
                            label="V3",
                            v_model=("var_3", True),
                            **COMPACT_STYLE,
                        )
                    with vuetify.VCol(cols=9):
                        vuetify.VTextField(
                            type="number",
                            label="Var4",
                            v_model=("var_4", 3),
                            **COMPACT_STYLE,
                        )
                with vuetify.VRow():
                    with vuetify.VCol():
                        vuetify.VTextField(
                            label="V5",
                            v_model=("var_5", "0, 1000, 2000, ..."),
                            **COMPACT_STYLE,
                        )
                    with vuetify.VCol():
                        vuetify.VTextField(
                            label="V6",
                            v_model=("var_6", "0, 1000, 2000, ..."),
                            **COMPACT_STYLE,
                        )
                    with vuetify.VCol():
                        vuetify.VSwitch(
                            label="V7",
                            v_model=("var_7", False),
                            **COMPACT_STYLE,
                        )
                with vuetify.VRow():
                    vuetify.VBtn("Run Simulation", click=ctrl.simulation_run)
                    vuetify.VBtn("Load Simulation Results/Open Data", click=ctrl.simulation_load)

            with vuetify.VCol(cols=8): # Right column
                with vuetify.VRow():
                    with vuetify.VCol():
                        fig = plotly.Figure()
                        ctrl.fig_1_update = fig.update
                    with vuetify.VCol():
                        html.Div("Ray selection widget (TODO)")
                with vuetify.VRow():
                    view = vtk.VtkRemoteView(ctrl.get_vtk_renderwindow(), interactive_ratio=1)
                    ctrl.fig_3_update = view.update
                    ctrl.fig_3_reset_camera = view.reset_camera
