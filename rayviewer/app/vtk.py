from pathlib import Path
import json

# VTK factory initialization
from vtkmodules import vtkRenderingOpenGL2  # noqa

from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkIOLegacy import vtkDataSetReader
from vtkmodules.vtkRenderingCore import vtkDiscretizableColorTransferFunction
from vtkmodules.vtkCommonExecutionModel import vtkTrivialProducer
from vtkmodules.vtkCommonDataModel import vtkPartitionedDataSet
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor

from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkCompositePolyDataMapper,
)


def get_reader(file_path):
    file_path = Path(file_path)
    ext = file_path.suffix

    reader = None

    if ext == ".vtu":
        reader = vtkXMLUnstructuredGridReader()

    if ext == ".vtk":
        reader = vtkDataSetReader()

    if reader:
        full_path = str(file_path.resolve().absolute())
        print(f"Loading: {full_path}")
        reader.SetFileName(full_path)
        reader.Update()

    return reader


class BaseElement:
    def __init__(self, filters, mapper, actor):
        self._filters = filters
        self._mapper = mapper
        self._actor = actor

        for i, filter in enumerate(filters):
            if i == len(filters) - 1:
                self._mapper.SetInputConnection(filter.GetOutputPort())
            else:
                filters[i + 1].SetInputConnection(filter.GetOutputPort())

        self._actor.SetMapper(self._mapper)

    @property
    def filters(self):
        return self._filters

    @property
    def mapper(self):
        return self._mapper

    @property
    def actor(self):
        return self._actor

    @property
    def property(self):
        return self._actor.GetProperty()

    def update(self):
        self.mapper.Update()


class MultiFileDataSet:
    def __init__(self, *paths):
        self.geo = vtkCompositeDataGeometryFilter()
        self.algo = vtkTrivialProducer()
        ds = vtkPartitionedDataSet()
        ds.SetNumberOfPartitions(len(paths))
        for i, f_path in enumerate(paths):
            reader = get_reader(f_path)
            ds.SetPartition(i, reader.GetOutput())

        self.geo.SetInputData(ds)
        self.geo.Update()

        self.algo.SetOutput(self.geo.GetOutput())


class GeometryElement(BaseElement):
    def __init__(self, reader, lut, composite):
        mapper = vtkCompositePolyDataMapper() if composite else vtkDataSetMapper()
        mapper.SetLookupTable(lut)
        mapper.UseLookupTableScalarRangeOn()
        actor = vtkActor()
        super().__init__([reader], mapper, actor)


class TubeElement(BaseElement):
    def __init__(self, reader, lut, composite):
        mapper = vtkCompositePolyDataMapper() if composite else vtkDataSetMapper()
        mapper.SetLookupTable(lut)
        mapper.UseLookupTableScalarRangeOn()
        actor = vtkActor()
        tube = vtkTubeFilter()
        tube.SetNumberOfSides(24)
        super().__init__([reader, tube], mapper, actor)

    @property
    def tube_filter(self):
        return self.filters[-1]


class VisualizationManager:
    def __init__(self):
        self._pipeline = []
        self._tube_indexes = []
        self._presets = ColorMaps()
        self._lut = vtkDiscretizableColorTransferFunction()
        self._scalar_bar = vtkScalarBarActor()
        self._scalar_bar.SetLookupTable(self._lut)
        self._scalar_bar.SetOrientationToHorizontal()
        self._scalar_bar.SetPosition(0.1, 0)
        self._scalar_bar.SetPosition2(0.8, 0.05)
        self._scalar_bar.SetHeight(0.1)

        self.renderer = vtkRenderer()
        self.renderer.SetBackground(0.35, 0.35, 0.35)
        self.renderer.AddActor2D(self._scalar_bar)

        self.render_window = vtkRenderWindow()
        self.render_window.AddRenderer(self.renderer)
        self.render_window.OffScreenRenderingOn()

        self.interactor = vtkRenderWindowInteractor()
        self.interactor.SetRenderWindow(self.render_window)

        style = vtkInteractorStyleSwitch()
        style.SetCurrentStyleToTrackballCamera()
        self.interactor.SetInteractorStyle(style)

        self.axes_actor = vtkAxesActor()
        self.orientation_widget = vtkOrientationMarkerWidget()
        self.orientation_widget.SetOrientationMarker(self.axes_actor)
        self.orientation_widget.SetInteractor(self.interactor)
        self.orientation_widget.SetViewport(0, 0.0, 0.2, 0.2)
        self.orientation_widget.SetEnabled(1)
        self.orientation_widget.InteractiveOff()

    def update_color_preset(self, name):
        x, colors = self._presets.get_colors(name)
        color_range_target = [100, 600]
        color_range_delta = color_range_target[1] - color_range_target[0]

        self._lut.RemoveAllPoints()
        for i, color in enumerate(colors):
            new_x = (
                color_range_delta * (x[i] - x[0]) / (x[-1] - x[0])
                + color_range_target[0]
            )
            self._lut.AddRGBPoint(new_x, *color)

        self._lut.Build()

    def add_geometry(self, source, composite=False):
        elem = GeometryElement(source, self._lut, composite)
        self._pipeline.append(elem)
        self.renderer.AddActor(elem.actor)
        self.renderer.ResetCamera()

    def add_tube_geometry(self, source, composite=False):
        self._tube_indexes.append(len(self._pipeline))
        elem = TubeElement(source, self._lut, composite)
        self._pipeline.append(elem)
        self.renderer.AddActor(elem.actor)

    def update_tube_radius(self, radius):
        for i in self._tube_indexes:
            elem = self._pipeline[i]
            elem.tube_filter.SetRadius(radius)

    def get_geometry(self, index):
        if len(self._pipeline):
            return self._pipeline[index]

    @property
    def preset_names(self):
        return self._presets.get_names()


class ColorMaps:
    def __init__(self):
        self._cmaps = {}
        with open(Path(__file__).with_name("colormaps.json")) as f:
            raw_cmaps = json.load(f)
            for raw_cmap in raw_cmaps:
                name = raw_cmap["Name"]
                key = name.lower()
                rgb_array = raw_cmap.get("RGBPoints")
                if rgb_array is None:
                    continue

                x = []
                colors = []
                for i in range(len(rgb_array) // 4):
                    x.append(i * 4)
                    colors.append(
                        (
                            rgb_array[i * 4 + 1],
                            rgb_array[i * 4 + 2],
                            rgb_array[i * 4 + 3],
                        )
                    )

                self._cmaps[key] = {"key": key, "name": name, "colors": colors, "x": x}

    def get_colors(self, key):
        return self._cmaps[key]["x"], self._cmaps[key]["colors"]

    def get_names(self):
        return list(self._cmaps.keys())
