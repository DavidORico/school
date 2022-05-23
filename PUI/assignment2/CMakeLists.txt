cmake_minimum_required(VERSION 3.20)
project(assignment2)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "-std=c++11 -Wall -pedantic -O3 ")

include_directories(src)

add_executable(assignment2
        src/common.h
        src/ff_replan.h
        src/main.cpp
        src/mcts.h
        src/value_iteration.h
        src/evaluate.h)
