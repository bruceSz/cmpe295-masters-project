# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.2

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/student/objectDetection/faster-rcnn-resnet/caffe-fast-rcnn

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/student/objectDetection/faster-rcnn-resnet/caffe-fast-rcnn/build

# Utility rule file for pytest.

# Include the progress variables for this target.
include CMakeFiles/pytest.dir/progress.make

CMakeFiles/pytest:
	cd /home/student/objectDetection/faster-rcnn-resnet/caffe-fast-rcnn/python && python2 -m unittest discover -s caffe/test

pytest: CMakeFiles/pytest
pytest: CMakeFiles/pytest.dir/build.make
.PHONY : pytest

# Rule to build all files generated by this target.
CMakeFiles/pytest.dir/build: pytest
.PHONY : CMakeFiles/pytest.dir/build

CMakeFiles/pytest.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/pytest.dir/cmake_clean.cmake
.PHONY : CMakeFiles/pytest.dir/clean

CMakeFiles/pytest.dir/depend:
	cd /home/student/objectDetection/faster-rcnn-resnet/caffe-fast-rcnn/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/student/objectDetection/faster-rcnn-resnet/caffe-fast-rcnn /home/student/objectDetection/faster-rcnn-resnet/caffe-fast-rcnn /home/student/objectDetection/faster-rcnn-resnet/caffe-fast-rcnn/build /home/student/objectDetection/faster-rcnn-resnet/caffe-fast-rcnn/build /home/student/objectDetection/faster-rcnn-resnet/caffe-fast-rcnn/build/CMakeFiles/pytest.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/pytest.dir/depend

