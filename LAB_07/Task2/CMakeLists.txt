cmake_minimum_required(VERSION 3.16)
project(viksov_fejs_laboratorij)

FIND_PACKAGE(OpenCV REQUIRED)

if(OpenCV_FOUND)
    include_directories(${OpenCV_INCLUDE_DIRS}) 
    add_executable(viksov_fejs_laboratorij objectDetection.cpp) 
    target_link_libraries(viksov_fejs_laboratorij ${OpenCV_LIBRARIES}) 
endif()

