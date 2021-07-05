import numpy as np
import healpy as hp
import vtk
import warnings
import sys

warnings.filterwarnings("ignore")

if len(sys.argv) <= 1:
    sys.exit("Error: No map in args")

map = sys.argv[1]

if not map.endswith('.fits'):
    sys.exit("Error: File not in FITS format")


# Loading FITS file 
# 
m = hp.read_map(map, 0) * 1e3

print(type(m))
print(len(m))
print('Max: {}'.format(m.max()))
print('Min: {}'.format(m.min()))

nside = hp.npix2nside(len(m))                               # Healpix resolution

xsize = ysize = 1000

vmin = -1e3; vmax = 1e3

theta = np.linspace(np.pi, 0, ysize)
phi = np.linspace(-np.pi, np.pi, xsize)

PHI, THETA = np.meshgrid(phi, theta)
grid_pix = hp.ang2pix(nside, THETA, PHI)
grid_map = m[grid_pix]

# print(grid_pix)
# print(grid_map)

r = 0.3
x = r*np.sin(THETA)*np.cos(PHI)
y = r*np.sin(THETA)*np.sin(PHI)
z = r*np.cos(THETA)

points = vtk.vtkPoints()
cells = vtk.vtkCellArray()

Colors = vtk.vtkFloatArray()
Colors.SetNumberOfComponents(1)
Colors.SetName("Colors")

# pointSource = vtk.vtkProgrammableSource()
# output = pointSource.GetPolyDataOutput()
# output.SetPoints(points)1e3

for i in range(len(x)):
    for j in range(len(x[i])):
        array = np.array([x[i][j],y[i][j],z[i][j]])
        # print(x[i][j])
        # print(y[i][j])
        # print(z[i][j])
        id = points.InsertNextPoint(x[i][j],y[i][j],z[i][j])
        cells.InsertNextCell(1)
        cells.InsertCellPoint(id)
        Colors.InsertNextTuple1(grid_map[i][j])

    # print(i)


polydata = vtk.vtkPolyData()
polydata.SetPoints(points)
polydata.SetVerts(cells)
polydata.GetPointData().SetScalars(Colors)
print('---------------')
print(polydata.GetPoints())


# polydata.GetPointData().SetScalars(Colors)
# polydata.Modified()

# vmin = -0.1
# vmax = 0.25
mapper = vtk.vtkPolyDataMapper()
mapper.GetLookupTable().SetTableRange(vmin,vmax)
mapper.GetLookupTable().SetHueRange(0.6667, 0.0)
mapper.GetLookupTable().SetSaturationRange(0.8, 0.7)
mapper.SetScalarModeToUsePointData()
mapper.UseLookupTableScalarRangeOn()
# mapper.SetLookupTable(lut)
mapper.SetInputData(polydata)
# mapper.ScalarVisibilityOff()


# Actor for the Points 
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().BackfaceCullingOff()
actor.GetProperty().ShadingOff()
# actor.GetProperty().SetInterpolationToFlat()
actor.GetProperty().SetPointSize(2)


# Color Legend
scalarBar = vtk.vtkScalarBarActor()
scalarBar.SetLookupTable(mapper.GetLookupTable())
# scalarBar.GetLookupTable().SetHueRange(0.6667, 0.0)
scalarBar.SetTitle("Temperature (mK)")
scalarBar.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
scalarBar.GetPositionCoordinate().SetValue(0.15,0.01)
scalarBar.SetOrientationToHorizontal()
scalarBar.SetWidth(0.7)
scalarBar.SetHeight(0.10)
# Test the Get/Set Position 
scalarBar.SetPosition(scalarBar.GetPosition())



ren = vtk.vtkRenderer()
ren.AddActor(actor)
ren.AddActor2D(scalarBar)
renWin = vtk.vtkRenderWindow()
renWin.SetSize(1000,1000)
renWin.AddRenderer(ren)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# while True:

#     renWin.Render()
#     ren1.GetActiveCamera().Azimuth( 1 )
#     iren.Start()

renWin.Render()
iren.Start()


# contour = vtk.vtkContourFilcdter()
# contour.SetInputConnection(points.GetOutputPort())
# contour.Update()

# lut = vtk.vtkLookupTable()
# lut.SetHueRange(0.6667, 0.0)

# l = points.GetData()
# print(l)

# surf = vtk.vtkSurfaceReconstructionFilter()
# surf.SetInputConnection(pointSource.GetOutputPort())

# cf = vtk.vtkContourFilter()
# cf.SetInputConnection(surf.GetOutputPort())
# cf.SetValue(0, 0.0)

# reverse = vtk.vtkReverseSense()
# reverse.SetInputConnection(cf.GetOutputPort())
# reverse.ReverseCellsOn()
# reverse.ReverseNormalsOn()



# dss = vtk.vtkDataSetSurfaceFilter()
# dss.SetInputConnection( d3D.GetOutputPort() )
# dss.Update()

# # Now we have our final polydata
# spherePoly = dss.GetOutput()