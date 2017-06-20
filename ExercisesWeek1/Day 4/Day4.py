# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#==============================================================================
# Challenge 1: Adding a new Filter+Mapper+Actor to visualize the grid 
#==============================================================================
import vtk

rectGridReader = vtk.vtkRectilinearGridReader()
rectGridReader.SetFileName("data/jet4_0.500.vtk")
rectGridReader.Update()

rectGridOutline = vtk.vtkRectilinearGridOutlineFilter()
rectGridOutline.SetInputData(rectGridReader.GetOutput())

rectGridGeom = vtk.vtkRectilinearGridGeometryFilter()
rectGridGeom.SetInputData(rectGridReader.GetOutput())

rectGridOutlineMapper = vtk.vtkPolyDataMapper()
rectGridOutlineMapper.SetInputConnection(rectGridOutline.GetOutputPort())

rectGridGeomMapper = vtk.vtkPolyDataMapper()
rectGridGeomMapper.SetInputConnection(rectGridGeom.GetOutputPort())

outlineActor = vtk.vtkActor()
outlineActor.SetMapper(rectGridOutlineMapper)
outlineActor.GetProperty().SetColor(1,1,1)

wireActor = vtk.vtkActor()
wireActor.SetMapper(rectGridGeomMapper)
wireActor.GetProperty().SetRepresentationToWireframe()
wireActor.GetProperty().SetColor(.8,.8,.8)

#==============================================================================
# Challenge 2: Using the vtkCalulator to compute the vector magnitude
#==============================================================================
magnitudeCalcFilter = vtk.vtkArrayCalculator()
magnitudeCalcFilter.SetInputConnection(rectGridReader.GetOutputPort())

magnitudeCalcFilter.AddVectorArrayName('vectors')
magnitudeCalcFilter.SetResultArrayName('magnitude')

magnitudeCalcFilter.SetFunction('mag(vectors)')
magnitudeCalcFilter.Update()

#Inspect the output of the calculator using the IPython console to verify the result
#%qtconsole

#==============================================================================
# Challenge 3: Visualize the data set as colored points based on the "magnitude" value
#==============================================================================
points = vtk.vtkPoints()
grid = magnitudeCalcFilter.GetOutput()
grid.GetPoints(points)
scalars = grid.GetPointData().GetArray('magnitude')

ugrid = vtk.vtkUnstructuredGrid()
ugrid.SetPoints(points)
ugrid.GetPointData().SetScalars(scalars)

for i in range (0, grid.GetNumberOfCells()):
    cell = grid.GetCell(i)
    ugrid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())

subset = vtk.vtkMaskPoints()
subset.SetOnRatio(30)
subset.RandomModeOn()
subset.SetInputData(ugrid)

pointsGlyph = vtk.vtkVertexGlyphFilter()
pointsGlyph.SetInputConnection(subset.GetOutputPort())
#pointsGlyph.SetInputData(ugrid)
pointsGlyph.Update()

pointsMapper = vtk.vtkPolyDataMapper()
pointsMapper.SetInputConnection(pointsGlyph.GetOutputPort())
pointsMapper.SetScalarModeToUsePointData()

pointsActor = vtk.vtkActor()
pointsActor.SetMapper(pointsMapper)

#==============================================================================
# Challenge 4: Visualize the data set as isosurfaces based on the "magnitude" value
#==============================================================================
scalarRange = ugrid.GetPointData().GetScalars().GetRange()

print(scalarRange)

isoFilter = vtk.vtkContourFilter()
isoFilter.SetInputData(ugrid)
isoFilter.GenerateValues(10, scalarRange)

isoMapper = vtk.vtkPolyDataMapper()
isoMapper.SetInputConnection(isoFilter.GetOutputPort())

isoActor = vtk.vtkActor()
isoActor.SetMapper(isoMapper)
isoActor.GetProperty().SetOpacity(0.5)

#==============================================================================
# # An alternative to define colormaps 
#==============================================================================
subset = vtk.vtkMaskPoints()
subset.SetOnRatio(10)
subset.RandomModeOn()
subset.SetInputConnection(rectGridReader.GetOutputPort())

lut = vtk.vtkLookupTable()
lut.SetNumberOfColors(256)
lut.SetHueRange(0.667, 0.0)
lut.SetVectorModeToMagnitude()
lut.Build()
isoMapper.SetLookupTable(lut)

hh = vtk.vtkHedgeHog()
hh.SetInputConnection(subset.GetOutputPort())
hh.SetScaleFactor(0.001)

hhm = vtk.vtkPolyDataMapper()
hhm.SetInputConnection(hh.GetOutputPort())
hhm.SetLookupTable(lut)
hhm.SetScalarVisibility(True)
hhm.SetScalarModeToUsePointFieldData()
hhm.SelectColorArray('vectors')
hhm.SetScalarRange((rectGridReader.GetOutput().GetPointData().GetVectors().GetRange(-1)))

hhmActor = vtk.vtkActor()
hhmActor.SetMapper(hhm)

#==============================================================================
# Usual rendering stuff.
#==============================================================================
renderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
 
#Add Actors
renderer.AddActor(outlineActor)
#renderer.AddActor(wireActor)
#renderer.AddActor(pointsActor)
#renderer.AddActor(isoActor)
renderer.AddActor(hhmActor)

renderer.SetBackground(.5,.5,.5)
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(60.0)
renderer.GetActiveCamera().Azimuth(30.0)
renderer.GetActiveCamera().Zoom(1.0)
 
renWin.SetSize(500, 500)
 
renWin.Render()
iren.Start()