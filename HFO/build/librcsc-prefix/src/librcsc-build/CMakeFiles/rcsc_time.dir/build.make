# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.6

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
CMAKE_COMMAND = /home/leno/anaconda3/envs/hfo/bin/cmake

# The command to remove a file.
RM = /home/leno/anaconda3/envs/hfo/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/leno/gitProjects/HFO_original/build/librcsc-prefix/src/librcsc

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/leno/gitProjects/HFO_original/build/librcsc-prefix/src/librcsc-build

# Include any dependencies generated for this target.
include CMakeFiles/rcsc_time.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/rcsc_time.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/rcsc_time.dir/flags.make

CMakeFiles/rcsc_time.dir/rcsc/time/timer.cpp.o: CMakeFiles/rcsc_time.dir/flags.make
CMakeFiles/rcsc_time.dir/rcsc/time/timer.cpp.o: /home/leno/gitProjects/HFO_original/build/librcsc-prefix/src/librcsc/rcsc/time/timer.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/leno/gitProjects/HFO_original/build/librcsc-prefix/src/librcsc-build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/rcsc_time.dir/rcsc/time/timer.cpp.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/rcsc_time.dir/rcsc/time/timer.cpp.o -c /home/leno/gitProjects/HFO_original/build/librcsc-prefix/src/librcsc/rcsc/time/timer.cpp

CMakeFiles/rcsc_time.dir/rcsc/time/timer.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/rcsc_time.dir/rcsc/time/timer.cpp.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/leno/gitProjects/HFO_original/build/librcsc-prefix/src/librcsc/rcsc/time/timer.cpp > CMakeFiles/rcsc_time.dir/rcsc/time/timer.cpp.i

CMakeFiles/rcsc_time.dir/rcsc/time/timer.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/rcsc_time.dir/rcsc/time/timer.cpp.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/leno/gitProjects/HFO_original/build/librcsc-prefix/src/librcsc/rcsc/time/timer.cpp -o CMakeFiles/rcsc_time.dir/rcsc/time/timer.cpp.s

CMakeFiles/rcsc_time.dir/rcsc/time/timer.cpp.o.requires:

.PHONY : CMakeFiles/rcsc_time.dir/rcsc/time/timer.cpp.o.requires

CMakeFiles/rcsc_time.dir/rcsc/time/timer.cpp.o.provides: CMakeFiles/rcsc_time.dir/rcsc/time/timer.cpp.o.requires
	$(MAKE) -f CMakeFiles/rcsc_time.dir/build.make CMakeFiles/rcsc_time.dir/rcsc/time/timer.cpp.o.provides.build
.PHONY : CMakeFiles/rcsc_time.dir/rcsc/time/timer.cpp.o.provides

CMakeFiles/rcsc_time.dir/rcsc/time/timer.cpp.o.provides.build: CMakeFiles/rcsc_time.dir/rcsc/time/timer.cpp.o


# Object files for target rcsc_time
rcsc_time_OBJECTS = \
"CMakeFiles/rcsc_time.dir/rcsc/time/timer.cpp.o"

# External object files for target rcsc_time
rcsc_time_EXTERNAL_OBJECTS =

lib/librcsc_time.a: CMakeFiles/rcsc_time.dir/rcsc/time/timer.cpp.o
lib/librcsc_time.a: CMakeFiles/rcsc_time.dir/build.make
lib/librcsc_time.a: CMakeFiles/rcsc_time.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/leno/gitProjects/HFO_original/build/librcsc-prefix/src/librcsc-build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX static library lib/librcsc_time.a"
	$(CMAKE_COMMAND) -P CMakeFiles/rcsc_time.dir/cmake_clean_target.cmake
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/rcsc_time.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/rcsc_time.dir/build: lib/librcsc_time.a

.PHONY : CMakeFiles/rcsc_time.dir/build

CMakeFiles/rcsc_time.dir/requires: CMakeFiles/rcsc_time.dir/rcsc/time/timer.cpp.o.requires

.PHONY : CMakeFiles/rcsc_time.dir/requires

CMakeFiles/rcsc_time.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/rcsc_time.dir/cmake_clean.cmake
.PHONY : CMakeFiles/rcsc_time.dir/clean

CMakeFiles/rcsc_time.dir/depend:
	cd /home/leno/gitProjects/HFO_original/build/librcsc-prefix/src/librcsc-build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/leno/gitProjects/HFO_original/build/librcsc-prefix/src/librcsc /home/leno/gitProjects/HFO_original/build/librcsc-prefix/src/librcsc /home/leno/gitProjects/HFO_original/build/librcsc-prefix/src/librcsc-build /home/leno/gitProjects/HFO_original/build/librcsc-prefix/src/librcsc-build /home/leno/gitProjects/HFO_original/build/librcsc-prefix/src/librcsc-build/CMakeFiles/rcsc_time.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/rcsc_time.dir/depend

