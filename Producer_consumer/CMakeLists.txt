#minimum cmake version required 
cmake_minimum_required(VERSION 3.10)

#Project name and language
project(ProducerConsumer CXX)

#set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED true)

#add executables
add_executable(producer_consumer producer_consumer.cpp)

#add pthread library for threading
find_package(Threads REQUIRED)

target_link_libraries(producer_consumer PRIVATE Threads::Threads)
