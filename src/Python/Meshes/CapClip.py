import vtk


def get_program_parameters():
    import argparse
    import sys
    if not len(sys.argv) > 1:
        return None
    description = 'Clip polydata using a plane.'
    epilogue = '''
    This is a simple example that uses vtkClipPolyData to clip input polydata, if provided, or a sphere otherwise.
    '''
    parser = argparse.ArgumentParser(description=description, epilog=epilogue)
    parser.add_argument('filename', help='Optional input filename e.g polydata.vtp.')
    args = parser.parse_args()
    return args.filename


def CapClip(filePath = None):
    # PolyData to process
    polyData = vtk.vtkPolyData()

    # Input optional polydata
    filePath = get_program_parameters()

    if filePath != None:
        reader = vtk.vtkXMLPolyDataReader()
        reader.SetFileName(filePath)
        reader.Update()
        polyData = reader.GetOutput()
        
    else:
        # Create a sphere
        sphereSource = vtk.vtkSphereSource()
        sphereSource.SetThetaResolution(20)
        sphereSource.SetPhiResolution(11)

        plane = vtk.vtkPlane()
        plane.SetOrigin(0, 0, 0)
        plane.SetNormal(1.0, -1.0, -1.0)

        clipper = vtk.vtkClipPolyData()
        clipper.SetInputConnection(sphereSource.GetOutputPort())
        clipper.SetClipFunction(plane)
        clipper.SetValue(0)
        clipper.Update()

        polyData = clipper.GetOutput()
        
    clipMapper = vtk.vtkDataSetMapper()
    clipMapper.SetInputData(polyData)

    colors = vtk.vtkNamedColors()

    clipActor = vtk.vtkActor()
    clipActor.SetMapper(clipMapper)
    clipActor.GetProperty().SetColor(colors.GetColor3d('Tomato'))
    clipActor.GetProperty().SetInterpolationToFlat()

    # Now extract feature edges
    boundaryEdges = vtk.vtkFeatureEdges()
    boundaryEdges.SetInputData(polyData)

    boundaryEdges.BoundaryEdgesOn()
    boundaryEdges.FeatureEdgesOff()
    boundaryEdges.NonManifoldEdgesOff()
    boundaryEdges.ManifoldEdgesOff()

    boundaryStrips = vtk.vtkStripper()
    boundaryStrips.SetInputConnection(boundaryEdges.GetOutputPort())
    boundaryStrips.Update()

    # Change the polylines into polygons
    boundaryPoly = vtk.vtkPolyData()
    boundaryPoly.SetPoints(boundaryStrips.GetOutput().GetPoints())
    boundaryPoly.SetPolys(boundaryStrips.GetOutput().GetLines())

    boundaryMapper = vtk.vtkPolyDataMapper()
    boundaryMapper.SetInputData(boundaryPoly)

    boundaryActor = vtk.vtkActor()
    boundaryActor.SetMapper(boundaryMapper)
    boundaryActor.GetProperty().SetColor(colors.GetColor3d("Banana"))

    # create render window, renderer and interactor
    renderWindow = vtk.vtkRenderWindow()
    renderer = vtk.vtkRenderer()
    renderWindow.AddRenderer(renderer)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renderWindow)

    # set background color
    renderer.SetBackground(colors.GetColor3d('steel_blue'))

    # add our actor to the renderer
    renderer.AddActor(clipActor)
    renderer.AddActor(boundaryActor)

    # Generate an interesting view
    renderer.ResetCamera()
    renderer.GetActiveCamera().Azimuth(30)
    renderer.GetActiveCamera().Elevation(30)
    renderer.GetActiveCamera().Dolly(1.2)
    renderer.ResetCameraClippingRange()

    renderWindow.Render()
    iren.Start()


if __name__ == '__main__':
    CapClip()