cmake_minimum_required(VERSION 3.15)
project(Day12)



set(CMAKE_CXX_STANDARD 14)

set(CMAKE_CXX_FLAGS "-Wall -Wextra -Werror -Wfatal-errors -Wshadow -pedantic")


add_executable(Day12
        day12code.cpp objects.cpp objects.hpp)
