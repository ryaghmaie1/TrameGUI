import logging
from pathlib import Path
import os
from .vtk import VisualizationManager, get_reader, MultiFileDataSet
from .chart import create_polar_fig
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from time import process_time
from os.path import dirname, join as pjoin
import scipy.io as sio
from time import localtime, strftime
import numpy as np
import pandas as pd
from collections import OrderedDict

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# COMPONENTS = ["R", "G", "B"]

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
    
    
        # index = self._server.state._pipeline
        # print('index=', index, flush=True)
        
        # self._viz.clear_pipeline()
        # FIXME
        base = Path(dataset_base_path)
        # base = Path(dataset_base_path)

        FileLoca = os.getcwd()+'/'+str(base)
        FileNameW = 'Wavelength'
        
        data_dir = pjoin(dirname(sio.__file__), FileLoca)
        mat_contentsW = sio.loadmat(data_dir+'/'+FileNameW+'.mat')
        wvln = mat_contentsW[FileNameW][0]
        Wavelength = np.asarray(wvln, dtype=object).tolist()
        # Wavelength.sort()
        COMPONENTS0 = Wavelength.copy()
        COMPONENTS = []
        if self._server.state.wvlt_chbx_450:
            COMPONENTS.append(COMPONENTS0[0])
        if self._server.state.wvlt_chbx_520:
            COMPONENTS.append(COMPONENTS0[1])
        if self._server.state.wvlt_chbx_620:
            COMPONENTS.append(COMPONENTS0[2])

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

        # # multi files
        for idx in range(9, 11):
            self._viz.add_geometry(get_reader(base / f"geometry{idx}.vtu"))

        self.ctrl.fig_3_reset_camera()


    def load_chbox(self, dataset_base_path, chbx_450, chbx_520, chbx_620):

        # self._viz.clear_pipeline()
        # FIXME
        base = Path(dataset_base_path)

        FileLoca = os.getcwd()+'/'+str(base)
        FileNameW = 'Wavelength'
        
        data_dir = pjoin(dirname(sio.__file__), FileLoca)
        mat_contentsW = sio.loadmat(data_dir+'/'+FileNameW+'.mat')
        wvln = mat_contentsW[FileNameW][0]
        Wavelength = np.asarray(wvln, dtype=object).tolist()
        # Wavelength.sort()
        COMPONENTS0 = Wavelength.copy()
        COMPONENTS = []
        if chbx_450:
            COMPONENTS.append(COMPONENTS0[0])
        if chbx_520:
            COMPONENTS.append(COMPONENTS0[1])
        if chbx_620:
            COMPONENTS.append(COMPONENTS0[2])

        # for idx in range(1, 5):
            # self._viz.add_geometry(get_reader(base / f"geometry{idx}.vtu"))

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

        # for idx in range(9, 11):
            # self._viz.add_geometry(get_reader(base / f"geometry{idx}.vtu"))

        self.ctrl.fig_3_reset_camera()

    def update_grid_fov(self, dataset_base_path, chbx_450, chbx_520, chbx_620, GD_output, grid):

        # self._viz.clear_pipeline()
        # FIXME
        base = Path(dataset_base_path)

        FileLoca = os.getcwd()+'/'+str(base)
        FileNameW = 'Wavelength'
        
        data_dir = pjoin(dirname(sio.__file__), FileLoca)
        mat_contentsW = sio.loadmat(data_dir+'/'+FileNameW+'.mat')
        wvln = mat_contentsW[FileNameW][0]
        Wavelength = np.asarray(wvln, dtype=object).tolist()
        # Wavelength.sort()
        COMPONENTS0 = Wavelength.copy()
        COMPONENTS = []
        if chbx_450:
            COMPONENTS.append(COMPONENTS0[0])
        if chbx_520:
            COMPONENTS.append(COMPONENTS0[1])
        if chbx_620:
            COMPONENTS.append(COMPONENTS0[2])

        # for idx in range(1, 5):
            # self._viz.add_geometry(get_reader(base / f"geometry{idx}.vtu"))

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

        # for idx in range(9, 11):
            # self._viz.add_geometry(get_reader(base / f"geometry{idx}.vtu"))

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

    def update_tube_radius(self, tube_radius=1000, **kwargs):
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

    @property
    def viz(self):
        return self._viz


def initialize(server):
    state, ctrl = server.state, server.controller
    engine = Engine(server)

    dir_to_list = Path("./data")
    state.available_directories = os.listdir(dir_to_list)
    # Dynamic wavelength checkbox
    state.wavelength = [
    ("450", "rgb(238, 130, 238)", True),
    ("520", "green", True),
    ("620", "red", True),
    ("630", "red", False),
    ]

    # Bind engine methods to controller
    ctrl.get_vtk_renderwindow = engine.get_renderwindow
    ctrl.update_visibility = engine.update_visibility
    state.change("tube_radius")(engine.update_tube_radius)
    state.change("tube_sides")(engine.update_tube_sides)
    state.change("tube_cap")(engine.update_tube_capping)
    state.change("color_preset")(engine.update_color_preset)

    @state.change("inp_nsub","inp_ntop","inp_devx","inp_devy")
    def create_plotly_fig(inp_nsub,inp_ntop,inp_devx,inp_devy,**kwargs):
        
        nSub = list(float(i) for i in inp_nsub.split(','))
        nTop = list(float(i) for i in inp_ntop.split(','))        
        devx = list(float(i) for i in inp_devx.split(','))
        devy = list(float(i) for i in inp_devy.split(','))        

        figks = go.Figure()
        
        figks.add_shape(type="circle",
            xref= 'x', yref="y",
            fillcolor='grey',
            x0=-1*nSub[0], y0=-1*nSub[0], x1=nSub[0], y1=nSub[0],
            line_color='grey',opacity=0.25,
        )
        figks.add_shape(type="circle",
            xref= 'x', yref="y",
            fillcolor="white",
            x0=-1*nTop[0], y0=-1*nTop[0], x1=nTop[0], y1=nTop[0],
            line_color="white",opacity=0.5,
        )
            
        figks.update_xaxes(range=[-1*nSub[0], nSub[0]], zeroline=False)
        figks.update_yaxes(range=[-1*nSub[0], nSub[0]])
        figks.update_layout(width=600, height=600,
                            title = "<b>Plot-1</b>")

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

        # figks.update_layout(clickmode="event",dragmode="select",editrevision="uirevision")
        # figks.config({'editable': True})
        
        # figks.update_layout.editrevision(config= dict({'editable': True}))
        
        # figks.update_layout.Shape(editable=True)
        # figks.layout.Shape(editable=True)
        
        return figks#.show(config=dict({'editable': True,'edits': {'shapePosition': True}}))

    @state.change("inp_devx","inp_devy")
    def create_plotly_fig4(inp_devx,inp_devy,**kwargs):
        
        devx = list(float(i) for i in state.inp_devx.split(','))
        devy = list(float(i) for i in state.inp_devy.split(','))       

        figks = go.Figure()

        if len(devx)==2 and len(devy)==2:
            figks.add_shape(type="rect",
                    xref= 'x', yref="y",
                    fillcolor='blue',
                    x0=devx[0], y0=devy[0],
                    x1=devx[1], y1=devy[1],
                    line_color='blue', opacity=0.25, name='boundary')
        else:
            figks.add_trace(go.Scatter(x=devx, y=devy, mode="lines", fill="toself", fillcolor='blue', line_color='blue', opacity=0.25, name='boundary'))
        
        wsz = 600
        figks.update_layout(width=wsz)
        
        figks.update_layout(title="<b>Plot-2</b>",\
            xaxis_title="<b>var-x</b>",\
            yaxis_title="<b>var-y</b>",\
            )
        
        figks.update_xaxes(range=[min(devx)-0.1*(max(devx)-min(devx)),max(devx)+0.1*(max(devx)-min(devx))])
        figks.update_yaxes(range=[min(devy)-0.1*(max(devy)-min(devy)),max(devy)+0.1*(max(devy)-min(devy))], scaleanchor = "x", scaleratio = 1)
        
        return figks

    @state.change("fig_1_size")
    def update_chart_size(fig_1_size, **kwargs):
        a = 2
        ctrl.fig_1_update(create_plotly_fig(state.inp_nsub,state.inp_ntop,state.inp_devx,state.inp_devy))
        
        # if fig_1_size:
            # ctrl.fig_1_update(create_plotly_fig(**fig_1_size.get("size")))
        
        # if fig_1_size:
            # ctrl.fig_1_update(create_polar_fig(**fig_1_size.get("size")))
            # ctrl.fig_1_update(figks)

    # @state.change("grid_dim_x", "grid_dim_y")
    # def update_grid(grid_dim_x, grid_dim_y, **kwargs):
        # grid_dim_x = int(grid_dim_x)
        # grid_dim_y = int(grid_dim_y)
        # grid = []
        # for j in range(grid_dim_y):
            # line = []
            # for i in range(grid_dim_x):
                # line.append(0)
            # grid.append(line)
        # state.grid = grid
        
    @state.change("fig_4_size")
    def update_chart_size4(fig_4_size, **kwargs):
        ctrl.fig_4_update(create_plotly_fig4(state.inp_devx,state.inp_devy))
        
    @state.change("inp_devx", "inp_devy")
    def update_grid(inp_devx, inp_devy, **kwargs):
        nx = 3
        ny = 3
        grid = []
        for j in range(ny):
            line = []
            for i in range(nx):
                line.append(0)
            grid.append(line)
        state.grid = grid

    @state.change("geometry_1_opacity")
    def update_geo_1_opacity(geometry_1_opacity, **kwargs):
        engine.update_opacity(0, geometry_1_opacity)

    @state.change("geometry_2_opacity")
    def update_geo_2_opacity(geometry_2_opacity, **kwargs):
        engine.update_opacity(1, geometry_2_opacity)

    @state.change("data_directory")
    def load_dataset(data_directory, **kwargs):
        if data_directory is None:
            return
        
        engine._viz.clear_pipeline()
        engine.update_visibility
        
        if np.sum(state.grid)==0:
            grid=[[1]]
        else:
            grid=state.grid
        nx = np.size(grid,1)
        ny = np.size(grid,0)
        for row in range(np.size(grid,1)):
            for col in range(np.size(grid,0)):
                if grid[row][col]:
                    rowt = nx-row
                    colt = col+1
                    fldnam = "grid-"+str(colt)+"-"+str(rowt)
                    
                    # FIXME
                    fldnam = data_directory+'/'+fldnam
                    full_path = Path(f"./data/{fldnam}")

                    engine.update_visibility
                    engine.load_dataset(full_path)
                    engine.update_tube_radius(state.tube_radius)
                    engine.update_tube_capping(state.tube_cap)
                    engine.update_tube_sides(state.tube_sides)
                    state.data_available = True
                    ctrl.fig_3_update()

    @state.change("wavelength")
    def readchkbox(wavelength, **kwargs):
    
        print('wavelength=',wavelength, flush=True)




    @state.change("data_directory", "wvlt_chbx_450", "wvlt_chbx_520", "wvlt_chbx_620")
    def load_chbox(data_directory, wvlt_chbx_450, wvlt_chbx_520, wvlt_chbx_620, **kwargs):
    
        if data_directory is None:
            return
            
        engine._viz.clear_pipeline()
        engine.update_visibility
        
        if np.sum(state.grid)==0:
            grid=[[1]]
        else:
            grid=state.grid
        nx = np.size(grid,1)
        ny = np.size(grid,0)
        for row in range(np.size(grid,1)):
            for col in range(np.size(grid,0)):
                if grid[row][col]:
                    rowt = nx-row
                    colt = col+1
                    fldnam = "grid-"+str(colt)+"-"+str(rowt)
                    # FIXME
                    fldnam = data_directory+'/'+fldnam                    
                    full_path = Path(f"./data/{fldnam}")

                    # engine.load_chbox(full_path, wvlt_chbx_450, wvlt_chbx_520, wvlt_chbx_620)
                    engine.update_visibility
                    engine.load_dataset(full_path)
                    engine.update_tube_radius(state.tube_radius)
                    engine.update_tube_capping(state.tube_cap)
                    engine.update_tube_sides(state.tube_sides)
                    state.data_available = True
                    ctrl.fig_3_update()

    @state.change("grid")
    def update_grid_pts(grid, **kwargs):
    
        if state.data_directory is None:
            return

        engine._viz.clear_pipeline()
        engine.update_visibility

        nx = np.size(grid,1)
        ny = np.size(grid,0)
                
        for row in range(np.size(grid,1)):
            for col in range(np.size(grid,0)):
                if grid[row][col]:
                    rowt = nx-row
                    colt = col+1

                    state.GD_output = (colt,rowt)
                    fldnam = "grid-"+str(colt)+"-"+str(rowt)
                    # FIXME
                    fldnam = state.data_directory+'/'+fldnam
                    full_path = Path(f"./data/{fldnam}")

                    engine.update_visibility
                    engine.load_dataset(full_path)
                    engine.update_tube_radius(state.tube_radius)
                    engine.update_tube_capping(state.tube_cap)
                    engine.update_tube_sides(state.tube_sides)
                    state.data_available = True
                    ctrl.fig_3_update()

    # Attach external execution to controller
    @ctrl.set("grating_plot")
    def plot_grating():
        ctrl.fig_1_update(create_plotly_fig(state.inp_nsub,state.inp_ntop,state.inp_devx,state.inp_devy))

    # Attach external execution to controller
    @ctrl.set("simulation_run")
    def run_simulation():
        a=6

    @ctrl.set("fig_3_reset_camera_x")
    def reset_camera_x():
        engine.viz.reset_camera_x()
        ctrl.fig_3_reset_camera()

    @ctrl.set("fig_3_reset_camera_y")
    def reset_camera_y():
        engine.viz.reset_camera_y()
        ctrl.fig_3_reset_camera()

    @ctrl.set("fig_3_reset_camera_z")
    def reset_camera_z():
        engine.viz.reset_camera_z()
        ctrl.fig_3_reset_camera()

    @ctrl.add("on_server_reload")
    def reload():
        # Fake to fillup the chart
        # ctrl.fig_1_update(create_polar_fig())        
        ctrl.fig_4_update(create_plotly_fig4(state.inp_devx,state.inp_devy))
        
    return engine
