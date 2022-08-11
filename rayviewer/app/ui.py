from trame.ui.vuetify import VAppLayout
from trame.widgets import vuetify, vtk, plotly, html, trame
import plotly.graph_objects as go

COMPACT = dict(dense=True, hide_details=True)

H_LINE_STYLE = "background: linear-gradient(180deg, rgba(0,0,0,0) calc(5% - 50px), rgba(100,192,192,10) calc(5%), rgba(0,0,0,0) calc(5% + 50px));"
V_LINE_STYLE = "background: linear-gradient(90deg, rgba(0,0,0,0) calc(5% - 50px), rgba(100,192,192,10) calc(5%), rgba(0,0,0,0) calc(5% + 50px));"

def on_event(type, e):
    print(type, e)

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
        # html.Div(f"Geometry {index + 1}", style="vertical-align: middle")
        if index==0:
            html.Div(f"geom-1", style="vertical-align: middle")
        elif index==1:
            html.Div(f"geom-2", style="vertical-align: middle")
        elif index==2:
            html.Div(f"geom-3", style="vertical-align: middle")
        elif index==3:
            html.Div(f"geom-4", style="vertical-align: middle")
        elif index==4:
            html.Div(f"geom-7", style="vertical-align: middle")
        elif index==5:
            html.Div(f"geom-8", style="vertical-align: middle")
        elif index==6:
            html.Div(f"geom-9", style="vertical-align: middle")
        elif index==7:
            html.Div(f"geom-10", style="vertical-align: middle")
        elif index==8:
            html.Div(f"geom-5", style="vertical-align: middle")
        elif index==9:
            html.Div(f"geom-6", style="vertical-align: middle")
    return container

# def create_dragfigure(width=600, height=600, **kwargs):
    # figks = go.Figure()

    # figks.add_shape(type="circle",
        # xref= 'x', yref="y",
        # fillcolor='grey',
        # x0=-2, y0=-2, x1=2, y1=2,
        # line_color='grey',opacity=0.25,
    # )
    # figks.add_shape(type="circle",
        # xref= 'x', yref="y",
        # fillcolor="white",
        # x0=-1, y0=-1, x1=1, y1=1,
        # line_color="white",opacity=0.5,
    # )

    # figks.update_xaxes(range=[-2, 2], zeroline=False)
    # figks.update_yaxes(range=[-2, 2])
    # figks.update_layout(width=600, height=600,
                        # title = "<b>Plot-1</b>")

    # devx = [0, 0.1]
    # devy = [0, 0.1]
    # figks.add_shape(type="rect",
        # xref= 'x', yref="y",
        # fillcolor='blue',
        # x0=devx[0], y0=devy[0],
        # x1=devx[1], y1=devy[1],
        # line_color='blue',opacity=0.75, editable=True
    # )


    # figks.add_shape(type="rect",
        # xref= 'x', yref="y",
        # fillcolor='red',
        # x0=1.2, y0=-1.2,
        # x1=1.3, y1=-1.3,
        # line_color='red',opacity=0.75, editable=True
    # )

    # figks.add_shape(type="rect",
        # xref= 'x', yref="y",
        # fillcolor='green',
        # x0=1.5, y0=0,
        # x1=1.6, y1=0.1,
        # line_color='green',opacity=0.75, editable=True
    # )

    # return figks

def initialize(server):
    state, ctrl = server.state, server.controller
    state.trame__title = "RayViewer"
    
    # def on_relayout(event=None):
        # print("relayout", event)
        # state.shapes = event

    with VAppLayout(server) as layout:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            # Settings parameters
            with vuetify.VCol(cols=4, classes="fill-height"):  # Left column
                with vuetify.VCard():
                    with vuetify.VCardTitle("Configuration", classes="py-0"):
                        vuetify.VSpacer()
                        # with vuetify.VBtn(
                            # icon=True, x_small=True, click=ctrl.on_server_reload
                        # ):
                            # vuetify.VIcon("mdi-refresh", small=True)

                    vuetify.VDivider()
                    with vuetify.VCardText():
                        with vuetify.VRow():
                            vuetify.VTextField(
                                label="var-1",
                                v_model=("inp_devx", "-0.3, 0.3"),
                                classes="mx-2",
                            )
                        with vuetify.VRow():
                            vuetify.VTextField(
                                label="var-2",
                                v_model=("inp_devy", "-0.2, 0.2"),
                                classes="mx-2",
                            )
                        with vuetify.VRow():
                            vuetify.VTextField(
                                label="var-3",
                                v_model=("inp_thck", "10"),
                                classes="mx-2",
                            )
                        with vuetify.VRow():
                            vuetify.VTextField(
                                label="var-4",
                                v_model=("inp_nsub", "2"),
                                classes="mx-2",
                            )
                        with vuetify.VRow():
                            vuetify.VTextField(
                                label="var-5",
                                v_model=("inp_ntop", "1"),
                                classes="mx-2",
                            )
                            
                        with vuetify.VRow():
                            with vuetify.VRadioGroup(
                                label="var-6",
                                v_model=("inp_IC_shap", "B"),
                                row=True,
                                classes="mx-2",
                            ):
                                vuetify.VRadio(label="C", value="A")
                                vuetify.VRadio(label="P", value="B")
                            with vuetify.VRadioGroup(
                                label="var-7",
                                v_model=("inp_IC_side", "A"),
                                row=True,
                                classes="mx-2",
                            ):
                                vuetify.VRadio(label="C", value="A")
                                vuetify.VRadio(label="P", value="B")
                        with vuetify.VRow(v_show="inp_IC_shap=='A'"):
                            vuetify.VTextField(
                                label="var-8",
                                v_model=("inp_ICx", "0,2000"),
                                classes="mx-2",
                                filled=True,
                            )
                        with vuetify.VRow(v_show="inp_IC_shap=='B'"):
                            vuetify.VTextField(
                                label="var-9",
                                v_model=("inp_ICy", "0,30"),
                                classes="mx-2",
                                filled=True,
                            )
                        with vuetify.VRow(v_show="inp_IC_shap=='B'"):
                            vuetify.VTextField(
                                label="var-10",
                                v_model=("inp_IC_peri", "350"),
                                classes="mx-2",
                            filled=True,
                            )
                        with vuetify.VRow():
                            vuetify.VTextField(
                                label="var-11",
                                v_model=("inp_IC_rota", "20"),
                                classes="mx-2",
                            filled=True,
                            )

                    with vuetify.VRow():
                        with vuetify.VCardActions():
                            vuetify.VBtn("Plot plot-1", click=ctrl.grating_plot)
                            
                        with vuetify.VCardActions():
                            vuetify.VBtn("Plot plot-2", click=ctrl.on_server_reload)
                            # vuetify.VBtn(icon=True, x_small=True, click=ctrl.on_server_reload):
                                # vuetify.VIcon("mdi-refresh", small=True)
                            
                        with vuetify.VCardActions():
                            vuetify.VBtn("Run run-1", click=ctrl.simulation_run)
                            
                # vuetify.VSpacer()
                vuetify.VDivider()
                # vuetify.VSpacer()
                with vuetify.VCard(classes="mt-6"):
                    with vuetify.VCardTitle("Load Results", classes="py-2"):
                        vuetify.VSpacer()
                        with vuetify.VRow():
                            with vuetify.VCardActions():
                                vuetify.VSelect(
                                    v_show="available_directories.length",
                                    classes="ml-4",
                                    v_model=("data_directory", None),
                                    items=("available_directories", []),
                                    **COMPACT,
                                )

                # Geometry control
                with vuetify.VCard(classes="mt-6", v_if=("data_available", False)):
                    with vuetify.VCardTitle("3D controls", classes="py-2"):
                        vuetify.VSpacer()
                        vuetify.VSelect(
                            v_model=("color_preset", "jet"),
                            items=("presets", []),
                            **COMPACT,
                            style="max-width: 50%;",
                        )
                    vuetify.VDivider()
                    with vuetify.VCardText():
                        with geometry_line(ctrl, 0):
                            vuetify.VSlider(
                                label="Opacity",
                                v_model=("geometry_1_opacity", 1),
                                min=0,
                                max=1,
                                step=0.05,
                                **COMPACT,
                                classes="ml-4",
                            )
                            html.Span("{{ Math.round(geometry_1_opacity * 100) }}%")
                        
                        with geometry_line(ctrl, 1):
                            vuetify.VSlider(
                                label="Opacity",
                                v_model=("geometry_2_opacity", 1),
                                min=0,
                                max=1,
                                step=0.05,
                                **COMPACT,
                                classes="ml-4",
                            )
                            html.Span("{{ Math.round(geometry_2_opacity * 100) }}%")

                        for i in range(2, 4):
                            geometry_line(ctrl, i)
                        for i in range(8, 10):
                            geometry_line(ctrl, i)

                        vuetify.VDivider()
                        with vuetify.VCardText():
                            with vuetify.VCardTitle("Wavelength", classes="py-0"):
                                vuetify.VSpacer()
                                # with vuetify.VRow(classes="align-center mt-2"):
                                    # vuetify.VCheckbox(
                                        # label="450",
                                        # v_model=("wvlt_chbx_450", True),
                                        # color='blue',
                                        # classes="mx-2")
                                    # vuetify.VCheckbox(
                                        # label="520",
                                        # v_model=("wvlt_chbx_520", True),
                                        # color='green',
                                        # classes="mx-2")
                                    # vuetify.VCheckbox(
                                        # label="620",
                                        # v_model=("wvlt_chbx_620", True),
                                        # color='red',
                                        # classes="mx-2")
                                with vuetify.VRow(classes="align-center mt-2"):
                                    vuetify.VCheckbox(
                                        v_for = "i10, index in wavelength",
                                        label=("i10[0]",),
                                        v_model=("i10[2]",),
                                        color=("i10[1]",),
                                        key = "index",
                                        change = "flushState('wavelength')",
                                        classes="mx-2")

                            vuetify.VDivider()
                            with html.Div(
                                classes="px-0 ma-0 d-flex flex-no-wrap",
                                style="flex: none; width: 100%;",
                            ):
                                with vuetify.VRow(classes="px-0 ma-0 pt-2"):
                                    with vuetify.VCardTitle("Grid Selector      ", classes="py-0"):
                                        vuetify.VSpacer()
                                        with vuetify.VCard(style="flex: none;", classes="ml-2"):
                                            with vuetify.VCardText(style="width: 100%;"):
                                    # with vuetify.VCardText():
                                        # with vuetify.VCardTitle("FoV Grid Selector", classes="py-4"):
                                                vuetify.VSpacer()
                                                # Make Grid from html
                                                with vuetify.VRow(
                                                    v_for="line, j in grid",
                                                    key="j",
                                                    classes="justify-center",
                                                    style=H_LINE_STYLE,
                                                ):
                                                    with html.Div(
                                                        v_for="item, i in line", key="i", style=V_LINE_STYLE
                                                    ):
                                                        with vuetify.VTooltip(left=True):
                                                            with vuetify.Template(
                                                                v_slot_activator="{ on, attrs }"
                                                            ):
                                                                with vuetify.VBtn(
                                                                    icon=True,
                                                                    small=False,
                                                                    color=("item ? 'red' : 'green'",),
                                                                    click="grid[j][i] = !grid[j][i];flushState('grid');",
                                                                    v_bind="attrs",
                                                                    v_on="on",
                                                                ):
                                                                    vuetify.VIcon(
                                                                        "mdi-checkbox-blank-circle"
                                                                    )
                                                            # vuetify.VTextField(v_model=("GD_output", (0, 0)))
                                                            html.Span("{{ i }} x {{ j }}")
                                                            
                                                            # vuetify.VTextField(v_model=("GD_output"),15)
                                                            
                                                # with vuetify.VCol(
                                                    # cols=8,
                                                    # classes="fill-height d-flex flex-column",
                                                # ):  # Right column
                                            with vuetify.VRow(classes="px-0 ma-0 pt-2",
                                                    # classes="justify-center",
                                                    # style=H_LINE_STYLE,
                                                    ):
                                                vuetify.VTextField(label="Thetax, Thetay (deg)",
                                                      v_model=("GD_output", (0, 0)),
                                                      classes="<b>px-0 ma-0</b>", color="red")

                            # vuetify.VRow()
                            vuetify.VSpacer()
                            vuetify.VDivider()
                            # vuetify.VSpacer()
                            vuetify.VSpacer()

                        for i in range(4, 6):
                            geometry_line(ctrl, i)


                        geometry_line(ctrl, 6)
                        with vuetify.VCol(classes="py-0"):
                            with vuetify.VRow(classes="align-center mt-2"):
                                vuetify.VSlider(
                                    label="Radius",
                                    v_model=("tube_radius", 1),
                                    min=1,
                                    max=1000,
                                    step=1,
                                    **COMPACT,
                                    classes="ml-4",
                                )
                                html.Span("{{ tube_radius }}")
                            with vuetify.VRow(classes="align-center mt-2"):
                                vuetify.VSlider(
                                    type="number",
                                    label="Sides",
                                    v_model=("tube_sides", 12),
                                    min=3,
                                    max=24,
                                    classes="ml-4",
                                    **COMPACT,
                                )
                                html.Span("{{ tube_sides }}")
                                html.Span("Capping", classes="ml-2")
                                vuetify.VSwitch(
                                    v_model=("tube_cap", True),
                                    **COMPACT,
                                    classes="mt-0 pt-0",
                                )

                        geometry_line(ctrl, 7)
                        # with vuetify.VCol(classes="py-0"):
                            # with vuetify.VRow(classes="align-center mt-2"):
                                # vuetify.VSlider(
                                    # label="Opacity (All Pupils)",
                                    # v_model=("pupils_opacity", 1),
                                    # min=0,
                                    # max=1,
                                    # step=0.05,
                                    # **COMPACT,
                                    # classes="ml-4",
                                    # )
                                # html.Span("{{ Math.round(pupils_opacity * 100) }}%")


                        # for i in range(8, 10):
                            # geometry_line(ctrl, i)
                        # for i in range(10, 12):
                            # geometry_line(ctrl, i)


            with vuetify.VCol(
                cols=8,
                classes="fill-height d-flex flex-column",
            ):  # Right column
                with html.Div(
                    classes="px-0 ma-0 d-flex flex-no-wrap",
                    style="flex: none; width: 100%;",
                ):
                    # with vuetify.VCard(classes="flex"):
                        # with vuetify.VCardText(style="height: 100%;"):
                    with vuetify.VRow(classes="px-0 ma-0 pt-2"):
                        with vuetify.VCard(style="flex: none;", classes="ml-2"):
                            with vuetify.VCardText(style="width: 100%;"):
                                # figure = plotly.Figure(
                                    # display_logo=True,
                                    # display_mode_bar="true",
                                    # selected=(on_event, "['selected', utils.safe($event)]"),
                                    # hover=(on_event, "['hover', utils.safe($event)]"),
                                    # selecting=(on_event, "['selecting', $event]"),
                                    # unhover=(on_event, "['unhover', $event]"),
                                # )
                                # ctrl.fig_1_update = figure.update
                                # # ctrl.fig_1_size
                            
                                with trame.SizeObserver("fig_1_size"):
                                    figure = plotly.Figure(
                                        display_logo=True,
                                        display_mode_bar="true",
                                        editable=True,
                                        edits=("{ shapePosition: true }",),
                                        __properties=["edits"],
                                        relayout=(on_relayout, "[$event]"),
                                        # selected=(on_event, "['selected', utils.safe($event)]"),
                                        # hover=(on_event, "['hover', utils.safe($event)]"),
                                        # selecting=(on_event, "['selecting', $event]"),
                                        # unhover=(on_event, "['unhover', $event]"),
                                    )
                                    ctrl.fig_1_update = figure.update
                            
                                # with vuetify.VRow():
                                    # with vuetify.VCol():
                                        # with trame.SizeObserver("fig_1_size"):
                                            # ctrl.fig_1_update = plotly.Figure(
                                                # create_dragfigure(),
                                                # display_mode_bar=("false",),
                                                # editable=True,
                                                # edits=("{ shapePosition: true }",),
                                                # __properties=["edits"],
                                                # relayout=(on_relayout, "[$event]"),
                                            # ).update
                                    # # with vuetify.VCol():
                                        # # html.Pre("{{ shapes }}")

                with html.Div(
                    classes="px-0 ma-0 d-flex flex-no-wrap",
                    style="flex: none; width: 100%;",
                ):
                    with vuetify.VRow(classes="px-0 ma-0 pt-2"):
                        with vuetify.VCard(style="flex: none;", classes="ml-2"):
                            with vuetify.VCardText(style="width: 100%;"):
                                with trame.SizeObserver("fig_4_size"):
                                    figure = plotly.Figure(
                                        display_logo=True,
                                        display_mode_bar="true",
                                        # selected=(on_event, "['selected', utils.safe($event)]"),
                                        # hover=(on_event, "['hover', utils.safe($event)]"),
                                        # selecting=(on_event, "['selecting', $event]"),
                                        # unhover=(on_event, "['unhover', $event]"),
                                    )
                                    ctrl.fig_4_update = figure.update

                # with html.Div(
                    # classes="px-0 ma-0 d-flex flex-no-wrap",
                    # style="flex: none; width: 100%;",
                # ):
                    # with vuetify.VRow(classes="px-0 ma-0 pt-2"):
                        # with vuetify.VCardTitle("FoV Grid Selector", classes="py-3"):
                            # vuetify.VSpacer()
                            # with vuetify.VCard(style="flex: none;", classes="ml-2"):
                                # with vuetify.VCardText(style="width: 100%;"):
                            # # with vuetify.VCard(style="flex: none;width: 100%", classes="ml-2"):
                                # # with vuetify.VCardTitle("FoV Grid Selector", classes="py-3"):
                                    # vuetify.VSpacer()
                                    # # Make Grid from html
                                    # with vuetify.VRow(
                                        # v_for="line, j in grid",
                                        # key="j",
                                        # classes="justify-center",
                                        # style=H_LINE_STYLE,
                                    # ):
                                        # with html.Div(
                                            # v_for="item, i in line", key="i", style=V_LINE_STYLE
                                        # ):
                                            # with vuetify.VTooltip(left=True):
                                                # with vuetify.Template(
                                                    # v_slot_activator="{ on, attrs }"
                                                # ):
                                                    # with vuetify.VBtn(
                                                        # icon=True,
                                                        # small=False,
                                                        # color=("item ? 'red' : 'green'",),
                                                        # click="grid[j][i] = !grid[j][i];flushState('grid');",
                                                        # v_bind="attrs",
                                                        # v_on="on",
                                                    # ):
                                                        # vuetify.VIcon(
                                                            # "mdi-checkbox-blank-circle"
                                                        # )
                                                # # vuetify.VTextField(v_model=("GD_output", (0, 0)))
                                                # html.Span("{{ i }} x {{ j }}")
                                                
                                                # # vuetify.VTextField(v_model=("GD_output"),15)
                                                
                                    # # with vuetify.VCol(
                                        # # cols=8,
                                        # # classes="fill-height d-flex flex-column",
                                    # # ):  # Right column
                                # with vuetify.VRow(classes="px-0 ma-0 pt-2",
                                        # # classes="justify-center",
                                        # # style=H_LINE_STYLE,
                                        # ):
                                    # vuetify.VTextField(label="Thetax, Thetay (deg)",
                                          # v_model=("GD_output", (0, 0)),
                                          # classes="<b>px-0 ma-0</b>", color="red")
                                                    
                                        # # with vuetify.VForm(classes="px-3"):
                                            # # vuetify.VTextField(label="Grid TextField",v_model=("GD_output"))
                                            # # vuetify.VTextarea(label="Grid TextArea Information",v_model=("GD_area_output"))


                # with html.Div(
                    # classes="px-0 ma-0 d-flex flex-no-wrap",
                    # style="flex: none; width: 100%;",
                # ):
                with vuetify.VRow(classes="px-0 ma-0 pt-2"):
                    with vuetify.VCard(
                        style="width: 100%;", v_if=("data_available", False)
                    ):
                        with vuetify.VCardTitle("3D Visualization", classes="py-0"):
                            vuetify.VSpacer()
                            with vuetify.VBtn(
                                x_small=True,
                                icon=True,
                                click=ctrl.fig_3_reset_camera_x,
                                color="red",
                                classes="ml-2",
                            ):
                                vuetify.VIcon("mdi-axis-x-arrow", small=True)

                            with vuetify.VBtn(
                                x_small=True,
                                icon=True,
                                click=ctrl.fig_3_reset_camera_y,
                                color="green",
                                classes="ml-2",
                            ):
                                vuetify.VIcon("mdi-axis-y-arrow", small=True)

                            with vuetify.VBtn(
                                x_small=True,
                                icon=True,
                                click=ctrl.fig_3_reset_camera_z,
                                color="blue",
                                classes="ml-2",
                            ):
                                vuetify.VIcon("mdi-axis-z-arrow", small=True)

                            with vuetify.VBtn(
                                x_small=True,
                                icon=True,
                                click=ctrl.fig_3_reset_camera,
                                classes="ml-2",
                            ):
                                vuetify.VIcon("mdi-crop-free", small=True)
                        with vuetify.VCardText(
                            classes="pa-0 ma-0",
                            style="height: calc(100% - 32px); overflow: hidden;",
                        ):
                            view = vtk.VtkRemoteView(
                                ctrl.get_vtk_renderwindow(),
                                interactive_ratio=1,
                            )
                            ctrl.fig_3_update = view.update
                            ctrl.fig_3_reset_camera = view.reset_camera