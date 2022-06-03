cmake_minimum_required(VERSION 3.20)
project(Viktor_Horvat)

FIND_PACKAGE(Boost)

IF (Boost_FOUND)
   	INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIR})
	add_executable(Viktor_Horvat viktor_horvat.cpp)
   	ADD_DEFINITIONS( "-DHAS_BOOST" )
ENDIF()

