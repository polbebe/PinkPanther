# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.13

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


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
CMAKE_SOURCE_DIR = /home/pi/Desktop/PinkPanther/Apriltag/apriltag-master

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/pi/PinkPanther/Apriltag/apriltag-master

# Utility rule file for apriltag_python.

# Include the progress variables for this target.
include CMakeFiles/apriltag_python.dir/progress.make

CMakeFiles/apriltag_python: apriltag.cpython-37m-arm-linux-gnueabihf.so


apriltag.cpython-37m-arm-linux-gnueabihf.so: libapriltag.so
apriltag.cpython-37m-arm-linux-gnueabihf.so: apriltag_pywrap.o
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/pi/PinkPanther/Apriltag/apriltag-master/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Generating apriltag.cpython-37m-arm-linux-gnueabihf.so"
	arm-linux-gnueabihf-gcc -pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions -Wl,-z,relro -lpython3.7m -Wl,-z,relro -Wl,-rpath,lib apriltag_pywrap.o /home/pi/PinkPanther/Apriltag/apriltag-master/libapriltag.so.3.1.0 -o apriltag.cpython-37m-arm-linux-gnueabihf.so

apriltag_pywrap.o: /home/pi/Desktop/PinkPanther/Apriltag/apriltag-master/apriltag_pywrap.c
apriltag_pywrap.o: apriltag_detect.docstring.h
apriltag_pywrap.o: apriltag_py_type.docstring.h
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/pi/PinkPanther/Apriltag/apriltag-master/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Generating apriltag_pywrap.o"
	/usr/bin/cc -Wno-unused-result -Wsign-compare -DNDEBUG -g -fwrapv -Wall -g -fstack-protector-strong -Wformat -Werror=format-security -g -flto -fuse-linker-plugin -ffat-lto-objects -fPIC -I/usr/include/python3.7m -I/usr/lib/python3/dist-packages/numpy/core/include -Wno-strict-prototypes -I/home/pi/PinkPanther/Apriltag/apriltag-master -c -o apriltag_pywrap.o /home/pi/Desktop/PinkPanther/Apriltag/apriltag-master/apriltag_pywrap.c

apriltag_detect.docstring.h:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/pi/PinkPanther/Apriltag/apriltag-master/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Generating apriltag_detect.docstring.h"
	< /home/pi/Desktop/PinkPanther/Apriltag/apriltag-master/apriltag_detect.docstring sed 's/"/\\"/g; s/^/"/; s/$$/\\n"/;' > apriltag_detect.docstring.h

apriltag_py_type.docstring.h:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/pi/PinkPanther/Apriltag/apriltag-master/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Generating apriltag_py_type.docstring.h"
	< /home/pi/Desktop/PinkPanther/Apriltag/apriltag-master/apriltag_py_type.docstring sed 's/"/\\"/g; s/^/"/; s/$$/\\n"/;' > apriltag_py_type.docstring.h

apriltag_python: CMakeFiles/apriltag_python
apriltag_python: apriltag.cpython-37m-arm-linux-gnueabihf.so
apriltag_python: apriltag_pywrap.o
apriltag_python: apriltag_detect.docstring.h
apriltag_python: apriltag_py_type.docstring.h
apriltag_python: CMakeFiles/apriltag_python.dir/build.make

.PHONY : apriltag_python

# Rule to build all files generated by this target.
CMakeFiles/apriltag_python.dir/build: apriltag_python

.PHONY : CMakeFiles/apriltag_python.dir/build

CMakeFiles/apriltag_python.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/apriltag_python.dir/cmake_clean.cmake
.PHONY : CMakeFiles/apriltag_python.dir/clean

CMakeFiles/apriltag_python.dir/depend:
	cd /home/pi/PinkPanther/Apriltag/apriltag-master && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/pi/Desktop/PinkPanther/Apriltag/apriltag-master /home/pi/Desktop/PinkPanther/Apriltag/apriltag-master /home/pi/PinkPanther/Apriltag/apriltag-master /home/pi/PinkPanther/Apriltag/apriltag-master /home/pi/PinkPanther/Apriltag/apriltag-master/CMakeFiles/apriltag_python.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/apriltag_python.dir/depend
