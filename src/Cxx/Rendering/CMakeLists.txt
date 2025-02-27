project (${WIKI}Rendering)

if(NOT VTK_BINARY_DIR)
  set(VTK_LIBRARIES "")
  find_package(VTK COMPONENTS
    vtkCommonColor
    CommonComputationalGeometry
    vtkCommonCore
    vtkCommonDataModel
    vtkCommonSystem
    vtkCommonTransforms
    vtkFiltersCore
    vtkFiltersGeneral
    vtkFiltersGeometry
    FiltersModeling
    vtkFiltersSources
    vtkIOGeometry
    vtkIOImage
    vtkIOLegacy
    vtkIOPLY
    vtkIOParallel
    vtkIOXML
    vtkImagingCore
    vtkImagingHybrid
    vtkImagingSources
    vtkInteractionImage
    vtkInteractionStyle
    InteractionWidgets
    RenderingAnnotation
    vtkRenderingContextOpenGL2
    vtkRenderingCore
    vtkRenderingFreeType
    vtkRenderingGL2PSOpenGL2
    vtkRenderingOpenGL2
    OPTIONAL_COMPONENTS
    vtkTestingRendering
    QUIET
    )
  if (VTK_VERSION VERSION_LESS "8.90.0")
    include(${VTK_USE_FILE})
  endif()
endif()

set(KIT_LIBS ${VTK_LIBRARIES})

set(RECENT_SRCS
  PBR_Skybox
  PBR_Skybox_Texturing
  PBR_Skybox_Anisotropy
)

#
# Build all .cxx files in the directory
file(GLOB ALL_FILES *.cxx)

if(VTK_VERSION VERSION_LESS "8.90.0")
  list(REMOVE_ITEM ALL_FILES ${RECENT_SRCS})
endif()

foreach(SOURCE_FILE ${ALL_FILES})
  string(REPLACE ".cxx" "" TMP ${SOURCE_FILE})
  string(REPLACE ${CMAKE_CURRENT_SOURCE_DIR}/ "" EXAMPLE ${TMP})
  add_executable(${WIKI}${EXAMPLE} ${EXECUTABLE_FLAG} ${EXAMPLE}.cxx)
  target_link_libraries(${WIKI}${EXAMPLE} ${KIT_LIBS})
  if (VTK_VERSION VERSION_GREATER "8.8")
    vtk_module_autoinit(
      TARGETS ${WIKI}${EXAMPLE}
      MODULES ${VTK_LIBRARIES}
      )
  endif()
endforeach()

if (BUILD_TESTING)
  # Testing
  set(KIT Rendering)
  set(NEEDS_ARGS
    FlatVersusGouraud
    HiddenLineRemoval
    InterpolateCamera
    MotionBlur
    Rainbow
    Rotations
    RotationsA
    RotationsB
    RotationsC
    RotationsD
    Shadows
    StripFran
    WalkCow
    WalkCowA
    WalkCowB
    )

  if(NOT VTK_VERSION VERSION_LESS "8.90.0")
    set(NEEDS_ARGS
        ${NEEDS_ARGS}
        ${RECENT_SRCS}
    )
  endif()

  set(DATA ${WikiExamples_SOURCE_DIR}/src/Testing/Data)
  set(TEMP ${WikiExamples_BINARY_DIR}/Testing/Temporary)

  add_test(${KIT}-FlatVersusGouraud ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${KIT}CxxTests
    TestFlatVersusGouraud ${DATA}/cow.obj)

  add_test(${KIT}-HiddenLineRemoval ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${KIT}CxxTests
    TestHiddenLineRemoval ${DATA}/cow.obj)

  add_test(${KIT}-InterpolateCamera ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${KIT}CxxTests
    TestInterpolateCamera ${DATA}/spider.ply)

  add_test(${KIT}-MotionBlur ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${KIT}CxxTests
    TestMotionBlur ${DATA}/Armadillo.ply)

  add_test(${KIT}-Rotations ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${KIT}CxxTests
    TestRotations ${DATA}/cow.obj)

  add_test(${KIT}-RotationsA ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${KIT}CxxTests
    TestRotationsA ${DATA}/cow.obj 1)

  add_test(${KIT}-RotationsB ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${KIT}CxxTests
    TestRotationsB ${DATA}/cow.obj 2)

  add_test(${KIT}-RotationsC ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${KIT}CxxTests
    TestRotationsC ${DATA}/cow.obj 3)

  add_test(${KIT}-RotationsD ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${KIT}CxxTests
    TestRotationsD ${DATA}/cow.obj 4)

  add_test(${KIT}-Rainbow ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${KIT}CxxTests
    TestRainbow ${DATA}/combxyz.bin ${DATA}/combq.bin)

  add_test(${KIT}-Shadows ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${KIT}CxxTests
    TestShadows ${DATA}/dragon.ply)

  add_test(${KIT}-StripFran ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${KIT}CxxTests
    TestStripFran ${DATA}/fran_cut.vtk)

  add_test(${KIT}-WalkCow ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${KIT}CxxTests
    TestWalkCow ${DATA}/cow.g)

  add_test(${KIT}-WalkCowA ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${KIT}CxxTests
    TestWalkCowA ${DATA}/cow.g 1)

  add_test(${KIT}-WalkCowB ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${KIT}CxxTests
    TestWalkCowB ${DATA}/cow.g 2)

  if(NOT VTK_VERSION VERSION_LESS "8.90.0")
    add_test(${KIT}-PBR_Skybox ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${KIT}CxxTests
      TestPBR_Skybox ${DATA}/Skyboxes/spiaggia_di_mondello_4k.hdr Boy)
    add_test(${KIT}-PBR_Skybox_Texturing ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${KIT}CxxTests
      TestPBR_Skybox_Texturing ${DATA}/Skyboxes/spiaggia_di_mondello_4k.hdr
       ${DATA}/Textures/Isotropic/vtk_Base_Color.png
       ${DATA}/Textures/Isotropic/vtk_Normal.png
       ${DATA}/Textures/Isotropic/vtk_Material.png
       ${DATA}/Textures/Isotropic/vtk_dark_bkg.png Boy)
    add_test(${KIT}-PBR_Skybox_Anisotropy ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${KIT}CxxTests
      TestPBR_Skybox_Anisotropy ${DATA}/Skyboxes/spiaggia_di_mondello_4k.hdr
       ${DATA}/Textures/Anisotropic/CarbonFiberAniso_albedo.png
       ${DATA}/Textures/Anisotropic/CarbonFiberAniso_normal.png
       ${DATA}/Textures/Anisotropic/CarbonFiberAniso_orm.png
       ${DATA}/Textures/Anisotropic/CarbonFiberAniso_anisotropyAngle.png Boy)
  endif()


  include(${WikiExamples_SOURCE_DIR}/CMake/ExamplesTesting.cmake)

endif()
