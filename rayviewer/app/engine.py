import logging
from pathlib import Path
from .vtk import VisualizationManager, get_reader, MultiFileDataSet
from .chart import create_polar_fig

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

COMPONENTS = ["R", "G", "B"]


class Engine:
    def __init__(self, server):
        self._server = server
        self._viz = VisualizationManager()
        self._viz.update_color_preset("cool to warm")
        server.state.presets = self._viz.preset_names

    @property
    def ctrl(self):
        return self._server.controller

    def load_dataset(self, dataset_base_path):
        base = Path(dataset_base_path)

        for idx in range(1, 5):
            self._viz.add_geometry(get_reader(base / f"geometry{idx}.vtu"))

        # multi files
        for geo_name in ["geometry5", "geometry6"]:
            f_names = [(base / f"{geo_name}_{c}.vtu") for c in COMPONENTS]
            self._viz.add_geometry(MultiFileDataSet(*f_names).algo, True)

        # tube multi files
        f_names = [(base / f"geometry7_{c}.vtk") for c in COMPONENTS]
        self._viz.add_tube_geometry(MultiFileDataSet(*f_names).algo, True)

        #  multi files
        f_names = [(base / f"geometry8_{c}.vtu") for c in COMPONENTS]
        self._viz.add_geometry(MultiFileDataSet(*f_names).algo, True)

        self.ctrl.fig_3_reset_camera()

    def update_visibility(self, index, visibility):
        geom = self._viz.get_geometry(index)
        if geom:
            geom.actor.SetVisibility(visibility)
            self.ctrl.fig_3_update()

    def update_opacity(self, index, opacity):
        geom = self._viz.get_geometry(index)
        if geom:
            geom.property.SetOpacity(opacity)
            self.ctrl.fig_3_update()

    def update_tube_radius(self, tube_radius=100, **kwargs):
        self._viz.update_tube_radius(tube_radius)
        self.ctrl.fig_3_update()

    def update_tube_capping(self, tube_cap=True, **kwargs):
        self._viz.update_tube_capping(tube_cap)
        self.ctrl.fig_3_update()

    def update_tube_sides(self, tube_sides=10, **kwargs):
        self._viz.update_tube_sides(tube_sides)
        self.ctrl.fig_3_update()

    def update_color_preset(self, color_preset, **kwargs):
        self._viz.update_color_preset(color_preset)
        self.ctrl.fig_3_update()

    def get_renderwindow(self):
        return self._viz.render_window


def initialize(server, dataset_path):
    state, ctrl = server.state, server.controller
    engine = Engine(server)

    # Bind engine methods to controller
    ctrl.get_vtk_renderwindow = engine.get_renderwindow
    ctrl.update_visibility = engine.update_visibility
    state.change("tube_radius")(engine.update_tube_radius)
    state.change("tube_sides")(engine.update_tube_sides)
    state.change("tube_cap")(engine.update_tube_capping)
    state.change("color_preset")(engine.update_color_preset)

    @state.change("fig_1_size")
    def update_chart_size(fig_1_size, **kwargs):
        if fig_1_size:
            ctrl.fig_1_update(create_polar_fig(**fig_1_size.get("size")))

    @state.change("grid_dim_x", "grid_dim_y")
    def update_grid(grid_dim_x, grid_dim_y, **kwargs):
        grid_dim_x = int(grid_dim_x)
        grid_dim_y = int(grid_dim_y)
        grid = []
        for j in range(grid_dim_y):
            line = []
            for i in range(grid_dim_x):
                line.append(0)
            grid.append(line)
        state.grid = grid

    @state.change("geometry_1_opacity")
    def update_geo_1_opacity(geometry_1_opacity, **kwargs):
        engine.update_opacity(0, geometry_1_opacity)

    @state.change("geometry_2_opacity")
    def update_geo_2_opacity(geometry_2_opacity, **kwargs):
        engine.update_opacity(1, geometry_2_opacity)

    # Attach external execution to controller
    @ctrl.set("simulation_run")
    def run_simulation():
        params = dict(
            v1=state.var_1,
            v2=state.var_2,
            v3=state.var_3,
            v4=state.var_4,
            v5=state.var_5,
            v6=state.var_6,
            v7=state.var_7,
        )
        print("Run external code", params)

    @ctrl.set("simulation_load")
    def load_simulation():
        params = dict(
            v1=state.var_1,
            v2=state.var_2,
            v3=state.var_3,
            v4=state.var_4,
            v5=state.var_5,
            v6=state.var_6,
            v7=state.var_7,
        )
        print("Load external code", params)

    @ctrl.add("on_server_ready")
    def load_dataset(**kwargs):
        engine.load_dataset(dataset_path)
        engine.update_tube_radius(state.tube_radius)

    @ctrl.add("on_server_reload")
    def reload():
        # Fake to fillup the chart
        ctrl.fig_1_update(create_polar_fig())

    return engine
