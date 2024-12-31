#cmake minimum version
cmake_minimum_required(VERSION 3.10)
#project name and langauge
project(TCPExample CXX)
#set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED true)

#add executables
add_executable(server server.cpp)
add_executable(client client.cpp)
#add pthread library for threading
find_package(Threads REQUIRED)

target_link_libraries(server PRIVATE Threads::Threads)
target_link_libraries(client PRIVATE Threads::Threads)

