import logging
from pathlib import Path
from .vtk import VisualizationManager, get_reader

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Engine:
    def __init__(self, server):
        self._server = server
        self._viz = VisualizationManager()

    @property
    def ctrl(self):
        return self._server.controller

    def load_dataset(self, dataset_base_path):
        base = Path(dataset_base_path)

        self._viz.add_geometry(get_reader(base / "geometry1.vtu"))
        self._viz.add_geometry(get_reader(base / "geometry2.vtu"))
        self._viz.add_geometry(get_reader(base / "geometry3.vtu"))
        self._viz.add_geometry(get_reader(base / "geometry4.vtu"))
        self._viz.add_geometry(get_reader(base / "geometry5_B.vtu")) # FIXME
        self._viz.add_geometry(get_reader(base / "geometry6_B.vtu")) # FIXME
        self._viz.add_tube_geometry(get_reader(base / "geometry7_B.vtu")) # FIXME
        self._viz.add_geometry(get_reader(base / "geometry8_B.vtu")) # FIXME

        self.ctrl.fig_3_reset_camera()

    def update_visibility(self, index, visibility):
        self._viz.get_geometry(index).actor.SetVisibility(visibility)
        self.ctrl.fig_3_update()

    def update_opacity(self, index, opacity):
        self._viz.get_geometry(index).property.SetOpacity(opacity)
        self.ctrl.fig_3_update()

    def update_tube_radius(self, tube_radius=100, **kwargs):
        self._viz.update_tube_radius(tube_radius)
        self.ctrl.fig_3_update()

    def update_color_preset(self, color_preset, **kwargs):
        pass

    def get_renderwindow(self):
        return self._viz.render_window




def initialize(server, dataset_base_path):
    state, ctrl = server.state, server.controller

    engine = Engine(server)
    engine.load_dataset(dataset_base_path)

    # Bind engine methods to controller
    ctrl.get_vtk_renderwindow = engine.get_renderwindow
    state.change("tube_radius")(engine.update_tube_radius)
    state.change("color_preset")(engine.update_color_preset)

    @state.change("geometry_1_opacity")
    def update_geo_1_opacity(geometry_1_opacity, **kwargs):
        engine.update_opacity(0, geometry_1_opacity)

    @state.change("geometry_2_opacity")
    def update_geo_2_opacity(geometry_2_opacity, **kwargs):
        engine.update_opacity(1, geometry_2_opacity)

    @ctrl.set("update_visibility")
    def update_visibility(index):
        visibility = state[f"visibility_{index}"]
        engine.update_visibility(index, visibility)

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

    return engine
