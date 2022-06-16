from trame.ui.vuetify import VAppLayout
from trame.widgets import vuetify, vtk, plotly, html

COMPACT = dict(dense=True, hide_details=True)


def geometry_line(ctrl, index):
    """Helper to build geometry control line"""
    container = None
    with vuetify.VRow(classes="align-center px-0 mx-0 py-1") as c:
        container = c
        vuetify.VCheckbox(
            on_icon="mdi-eye-outline",
            off_icon="mdi-eye-off-outline",
            v_model=(f"visibility_{index}", True),
            change=(ctrl.update_visibility, f"[{index}, $event]"),
            **COMPACT,
            classes="mt-0 pt-0",
        )
        html.Div(f"Geometry {index + 1}", style="vertical-align: middle")

    return container


def initialize(server):
    state, ctrl = server.state, server.controller
    state.trame__title = "RayViewer"

    with VAppLayout(server) as layout:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            # Settings parameters
            with vuetify.VCol(cols=4, classes="fill-height"):  # Left column
                with vuetify.VCard():
                    vuetify.VCardTitle("Configuration", classes="py-0")
                    vuetify.VDivider()
                    with vuetify.VCardText():
                        vuetify.VTextField(
                            label="Variable - 1",
                            v_model=("var_1", "0, 1000, 2000, ..."),
                        )
                        vuetify.VTextField(
                            label="Variable - 2",
                            v_model=("var_2", "0, 1000, 2000, ..."),
                        )
                        with vuetify.VRow():
                            with vuetify.VCol(cols=3):
                                vuetify.VSwitch(
                                    label="V3",
                                    v_model=("var_3", True),
                                )
                            with vuetify.VCol(cols=9):
                                vuetify.VTextField(
                                    type="number",
                                    label="Var4",
                                    v_model=("var_4", 3),
                                )
                        with vuetify.VRow():
                            vuetify.VTextField(
                                label="V5",
                                v_model=("var_5", "0, 1000, 2000, ..."),
                                classes="mx-2",
                            )
                            vuetify.VTextField(
                                label="V6",
                                v_model=("var_6", "0, 1000, 2000, ..."),
                                classes="mx-2",
                            )
                            vuetify.VSwitch(
                                label="V7",
                                v_model=("var_7", False),
                                classes="mx-2",
                            )
                    with vuetify.VCardActions():
                        vuetify.VBtn("Run Simulation", click=ctrl.simulation_run)
                        vuetify.VSpacer()
                        vuetify.VBtn("Load", click=ctrl.simulation_load)

                # Geometry control
                with vuetify.VCard(classes="mt-6"):
                    with vuetify.VCardTitle("3D controls", classes="py-2"):
                        vuetify.VSpacer()
                        vuetify.VSelect(
                            v_model=("color_preset", "cool to warm"),
                            items=("presets", []),
                            **COMPACT,
                            style="max-width: 50%;",
                        )
                    vuetify.VDivider()
                    with vuetify.VCardText():
                        with geometry_line(ctrl, 0):
                            vuetify.VSlider(
                                v_model=("geometry_0_opacity", 1),
                                min=0,
                                max=1,
                                step=0.05,
                                **COMPACT,
                            )
                            html.Span("{{ Math.round(geometry_0_opacity * 100) }}%")

                        with geometry_line(ctrl, 1):
                            vuetify.VSlider(
                                v_model=("geometry_1_opacity", 1),
                                min=0,
                                max=1,
                                step=0.05,
                                **COMPACT,
                            )
                            html.Span("{{ Math.round(geometry_1_opacity * 100) }}%")

                        for i in range(2, 6):
                            geometry_line(ctrl, i)

                        with geometry_line(ctrl, 6):
                            vuetify.VSlider(
                                label="Radius",
                                v_model=("tube_radius", 100),
                                min=50,
                                max=200,
                                step=1,
                                **COMPACT,
                                classes="ml-4",
                            )
                            html.Span("{{ tube_radius }}")

                        geometry_line(ctrl, 7)

            with vuetify.VCol(
                cols=8, classes="fill-height d-flex flex-column"
            ):  # Right column
                with vuetify.VRow(
                    classes="px-0 ma-0", style="min-height: 0; flex: none;"
                ):
                    with vuetify.VCol(classes="pa-0 ma-0"):
                        with vuetify.VCard():
                            with vuetify.VCardText():
                                fig = plotly.Figure(display_mode_bar=False)
                                ctrl.fig_1_update = fig.update

                    with vuetify.VCol(classes="pt-0 pr-0 ma-0"):
                        with vuetify.VCard():
                            with vuetify.VCardText():
                                html.Div("Ray selection widget (TODO)")
                                vuetify.VBtn("Reload", click=ctrl.on_server_reload)

                with vuetify.VRow(classes="px-0 ma-0 pt-2"):
                    with vuetify.VCard(style="width: 100%;"):
                        with vuetify.VCardTitle("3D Visualization", classes="py-0"):
                            vuetify.VSpacer()
                            with vuetify.VBtn(
                                x_small=True,
                                icon=True,
                                click=ctrl.fig_3_reset_camera,
                            ):
                                vuetify.VIcon("mdi-crop-free", small=True)
                        with vuetify.VCardText(
                            classes="pa-0 ma-0",
                            style="height: calc(100% - 32px); overflow: hidden;",
                        ):
                            view = vtk.VtkRemoteView(
                                ctrl.get_vtk_renderwindow(), interactive_ratio=1
                            )
                            ctrl.fig_3_update = view.update
                            ctrl.fig_3_reset_camera = view.reset_camera
