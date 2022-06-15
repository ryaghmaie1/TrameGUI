
from abc import ABC, abstractmethod
from pathlib import Path

# VTK factory initialization
from vtkmodules import vtkRenderingOpenGL2 # noqa

from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkIOXML import vtkXMLUnstructuredDataReader
from vtkmodules.vtkIOLegacy import vtkDataSetReader

from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

def get_reader(file_path):
    file_path = Path(file_path)
    ext = file_path.suffix

    reader = None

    if ext == ".vtu":
        reader = vtkXMLUnstructuredDataReader()

    if ext == ".vtk":
        reader = vtkDataSetReader()

    if reader:
        reader.SetFileName(str(file_path.resolve().absolute()))

    return reader

class BaseElement(ABC):
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

class GeometryElement(BaseElement):
    def __init__(self, reader):
        mapper = vtkDataSetMapper()
        actor = vtkActor()
        super().__init__([reader], mapper, actor)

class TubeElement(BaseElement):
    def __init__(self, reader):
        mapper = vtkDataSetMapper()
        actor = vtkActor()
        super().__init__([reader, vtkTubeFilter()], mapper, actor)

    @property
    def tube_filter(self):
        return self.filters[-1]

class VisualizationManager:
    def __init__(self):
        self._pipeline = []
        self._tube_indexes = []
        self.renderer = vtkRenderer()
        self.render_window = vtkRenderWindow()
        self.renderer.SetBackground(0.35, 0.35, 0.35)
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


    def add_geometry(self, source):
        elem = GeometryElement(source)
        self._pipeline.append(elem)
        self.renderer.AddActor(elem.actor)

    def add_tube_geometry(self, source):
        self._tube_indexes.append(len(self._pipeline))
        elem = TubeElement(source)
        self._pipeline.append(elem)
        self.renderer.AddActor(elem.actor)

    def update_tube_radius(self, radius):
        for i in self._tube_indexes:
            elem = self._pipeline[i]
            elem.tube_filter.SetRadius(radius)

    def get_geometry(self, index):
        return self._pipeline[index]
