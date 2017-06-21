import vtk

# Read the file (to test that it was written correctly)
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("/Users/sebastiansanchez/IngenieriaSistemas/2017-18/Visual/Visualization/ExercisesWeek2/data/wind_image.vti")
reader.Update()

# Convert the image to a polydata
imageDataGeometryFilter = vtk.vtkImageDataGeometryFilter()
imageDataGeometryFilter.SetInputConnection(reader.GetOutputPort())
imageDataGeometryFilter.Update()

##------------FILTER, MAPPER, AND ACTOR -------------------

scalarRange = reader.GetOutput().GetPointData().GetScalars().GetRange(-1)
contoursFilter = vtk.vtkContourFilter()
contoursFilter.SetInputConnection(imageDataGeometryFilter.GetOutputPort())
contoursFilter.GenerateValues(8, scalarRange)

# Create transfer mapping scalar value to opacity
opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(0.0, 0.0)
opacityTransferFunction.AddPoint(6.0, 1)
opacityTransferFunction.AddPoint(14.0, 1)
#opacityTransferFunction.AddPoint(0, 0.0)
#opacityTransferFunction.AddPoint(4, 0.2)
#opacityTransferFunction.AddPoint(7, 1)
#opacityTransferFunction.AddPoint(14, 1)

# Create transfer mapping scalar value to color
# Create transfer mapping scalar value to color
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0.0, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(0.5, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(2.0, 0.0, 0.0, 1.0)
colorTransferFunction.AddRGBPoint(6.0, 0.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(14.0, 0.0, 0.2, 0.0)

tableSize = 30
#
lut = vtk.vtkLookupTable()
lut.SetNumberOfTableValues(tableSize)
lut.Build()
#
for i in range(0,tableSize):
    rgb = list(colorTransferFunction.GetColor(float(i)/tableSize))+[0.5]
    lut.SetTableValue(i,rgb)

# Pass the streamlines to the mapper
streamlineMapper = vtk.vtkPolyDataMapper()
streamlineMapper.SetLookupTable(lut)
streamlineMapper.SetInputConnection(streamline.GetOutputPort())
streamlineMapper.SetScalarVisibility(True)
streamlineMapper.SetScalarModeToUsePointFieldData()
streamlineMapper.SelectColorArray('vectors')
# See documentation for the parameter in GetRange()
# http://www.vtk.org/doc/nightly/html/classvtkDataArray.html#ab7efccf59d099c038a4ae269a490e1a3
streamlineMapper.SetScalarRange((reader.GetOutput().GetPointData().GetVectors().GetRange(-1)))

# Pass the mapper to the actor
streamlineActor = vtk.vtkActor()
streamlineActor.SetMapper(streamlineMapper)
streamlineActor.GetProperty().SetLineWidth(2.0)

# Add the outline of the data set
gOutline = vtk.vtkRectilinearGridOutlineFilter()
gOutline.SetInputData(output)
gOutlineMapper = vtk.vtkPolyDataMapper()
gOutlineMapper.SetInputConnection(gOutline.GetOutputPort())
gOutlineActor = vtk.vtkActor()
gOutlineActor.SetMapper(gOutlineMapper)
gOutlineActor.GetProperty().SetColor(0.5,0.5,0.5)

# Rendering / Window
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(streamlineActor)
renderer.AddActor(outlineActor)
#renderer.AddActor(gOutlineActor)

renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.SetSize(500, 500)
renderWindow.Render()

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
interactor.SetRenderWindow(renderWindow)
interactor.Initialize()
interactor.Start()
