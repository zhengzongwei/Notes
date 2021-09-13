# CMake 版本号要求
cmake_miniMum_required(VERSION 2.8)

# 项目信息
project(Test)

# The version number.
set (Tutorial_VERSION_MAJOR 1)
set (Tutorial_VERSION_MINOR 0)

# PROJECT_SOURCE_DIR为cmake内置变量，表示工程的根目录
set(RELEASE_DIR ${PROJECT_SOURCE_DIR}/release)

# set(LIBRARY_OUTPUT_PATH ${RELEASE_DIR}/linux/${BuildType})
# set(EXECUTABLE_OUTPUT_PATH ${RELEASE_DIR}/linux/${BuildType})

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${RELEASE_DIR})
# set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# 查找当前目录下所有的源文件，并将名称保存到DIR_SRCS变量
aux_source_directory(. DIR_SRCS)

add_subdirectory(src)

# 指定生成目标
add_executable(demo main.c)

# 添加链接库
target_link_libraries(demo srcs)


