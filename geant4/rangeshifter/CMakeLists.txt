cmake_minimum_required(VERSION 3.3 FATAL_ERROR)

project(rangeshifter)

# Set build type to Release, enabling optimisation
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

set(CMAKE_CXX_FLAGS "-Wall -Wextra")
set(CMAKE_CXX_FLAGS_DEBUG "-g")
set(CMAKE_CXX_FLAGS_RELEASE "-O3")

option(WITH_GEANT4_UIVIS "Build with Geant4 UI and Vis drivers" ON)
if(WITH_GEANT4_UIVIS)
  find_package(Geant4 REQUIRED ui_all vis_all)
else()
  find_package(Geant4 REQUIRED)
endif()

include(${Geant4_USE_FILE})
include_directories(${PROJECT_SOURCE_DIR}/include)

# We presume the existence of three directories
file(GLOB_RECURSE sources ${PROJECT_SOURCE_DIR}/src/*.cc)
file(GLOB_RECURSE headers ${PROJECT_SOURCE_DIR}/include/*.hh)
file(GLOB_RECURSE macros RELATIVE ${PROJECT_SOURCE_DIR} macros/*.mac)
file(GLOB_RECURSE input RELATIVE ${PROJECT_SOURCE_DIR} *.txt)

# Enable macros for out-of-source build
foreach(_file ${macros})
  configure_file(
    ${_file}
    ${PROJECT_BINARY_DIR}/${_file}
    COPYONLY
    )

endforeach()

# Enable input files for out-of-source build
foreach(_file ${input})
  configure_file(
    ${_file}
    ${PROJECT_BINARY_DIR}/${_file}
    COPYONLY
    )

endforeach()

file(COPY ${PROJECT_SOURCE_DIR}/calorimeter_histogram.C
     DESTINATION ${PROJECT_BINARY_DIR})

file(COPY ${PROJECT_SOURCE_DIR}/calorimeter_histogram.py
     DESTINATION ${PROJECT_BINARY_DIR})

add_executable(rangeshifter main.cc ${sources} ${headers})
target_link_libraries(rangeshifter ${Geant4_LIBRARIES})

install(TARGETS rangeshifter DESTINATION bin)
