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
CMAKE_SOURCE_DIR = /home/leno/gitProjects/HFO_original

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/leno/gitProjects/HFO_original/build

# Utility rule file for soccerwindow2.

# Include the progress variables for this target.
include CMakeFiles/soccerwindow2.dir/progress.make

CMakeFiles/soccerwindow2: CMakeFiles/soccerwindow2-complete


CMakeFiles/soccerwindow2-complete: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-install
CMakeFiles/soccerwindow2-complete: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-mkdir
CMakeFiles/soccerwindow2-complete: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-download
CMakeFiles/soccerwindow2-complete: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-update
CMakeFiles/soccerwindow2-complete: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-patch
CMakeFiles/soccerwindow2-complete: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-configure
CMakeFiles/soccerwindow2-complete: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-build
CMakeFiles/soccerwindow2-complete: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-install
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/leno/gitProjects/HFO_original/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Completed 'soccerwindow2'"
	/home/leno/anaconda3/envs/hfo/bin/cmake -E make_directory /home/leno/gitProjects/HFO_original/build/CMakeFiles
	/home/leno/anaconda3/envs/hfo/bin/cmake -E touch /home/leno/gitProjects/HFO_original/build/CMakeFiles/soccerwindow2-complete
	/home/leno/anaconda3/envs/hfo/bin/cmake -E touch /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-done

soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-install: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-build
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/leno/gitProjects/HFO_original/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "No install step for 'soccerwindow2'"
	cd /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src/soccerwindow2-build && /home/leno/anaconda3/envs/hfo/bin/cmake -E echo_append
	cd /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src/soccerwindow2-build && /home/leno/anaconda3/envs/hfo/bin/cmake -E touch /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-install

soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-mkdir:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/leno/gitProjects/HFO_original/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Creating directories for 'soccerwindow2'"
	/home/leno/anaconda3/envs/hfo/bin/cmake -E make_directory /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src/soccerwindow2
	/home/leno/anaconda3/envs/hfo/bin/cmake -E make_directory /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src/soccerwindow2-build
	/home/leno/anaconda3/envs/hfo/bin/cmake -E make_directory /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix
	/home/leno/anaconda3/envs/hfo/bin/cmake -E make_directory /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/tmp
	/home/leno/anaconda3/envs/hfo/bin/cmake -E make_directory /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src/soccerwindow2-stamp
	/home/leno/anaconda3/envs/hfo/bin/cmake -E make_directory /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src
	/home/leno/anaconda3/envs/hfo/bin/cmake -E touch /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-mkdir

soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-download: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-gitinfo.txt
soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-download: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-mkdir
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/leno/gitProjects/HFO_original/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Performing download step (git clone) for 'soccerwindow2'"
	cd /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src && /home/leno/anaconda3/envs/hfo/bin/cmake -P /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/tmp/soccerwindow2-gitclone.cmake
	cd /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src && /home/leno/anaconda3/envs/hfo/bin/cmake -E touch /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-download

soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-update: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-download
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/leno/gitProjects/HFO_original/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "No update step for 'soccerwindow2'"
	cd /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src/soccerwindow2 && /home/leno/anaconda3/envs/hfo/bin/cmake -E echo_append
	cd /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src/soccerwindow2 && /home/leno/anaconda3/envs/hfo/bin/cmake -E touch /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-update

soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-patch: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-download
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/leno/gitProjects/HFO_original/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_6) "No patch step for 'soccerwindow2'"
	/home/leno/anaconda3/envs/hfo/bin/cmake -E echo_append
	/home/leno/anaconda3/envs/hfo/bin/cmake -E touch /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-patch

soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-configure: librcsc-prefix/src/librcsc-stamp/librcsc-done
soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-configure: soccerwindow2-prefix/tmp/soccerwindow2-cfgcmd.txt
soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-configure: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-update
soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-configure: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-patch
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/leno/gitProjects/HFO_original/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_7) "Performing configure step for 'soccerwindow2'"
	cd /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src/soccerwindow2-build && /home/leno/anaconda3/envs/hfo/bin/cmake -DCMAKE_BUILD_TYPE=MinSizeRel -DLIBRCSC_INCLUDE_DIR=/home/leno/gitProjects/HFO_original/build/librcsc-prefix/src/librcsc -DLIBRCSC_LINK_DIR=/home/leno/gitProjects/HFO_original/build/librcsc-prefix/src/librcsc-build/lib "-GUnix Makefiles" /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src/soccerwindow2
	cd /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src/soccerwindow2-build && /home/leno/anaconda3/envs/hfo/bin/cmake -E touch /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-configure

soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-build: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-configure
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/leno/gitProjects/HFO_original/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_8) "Performing build step for 'soccerwindow2'"
	cd /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src/soccerwindow2-build && $(MAKE)
	cd /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src/soccerwindow2-build && /home/leno/anaconda3/envs/hfo/bin/cmake -E touch /home/leno/gitProjects/HFO_original/build/soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-build

soccerwindow2: CMakeFiles/soccerwindow2
soccerwindow2: CMakeFiles/soccerwindow2-complete
soccerwindow2: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-install
soccerwindow2: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-mkdir
soccerwindow2: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-download
soccerwindow2: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-update
soccerwindow2: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-patch
soccerwindow2: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-configure
soccerwindow2: soccerwindow2-prefix/src/soccerwindow2-stamp/soccerwindow2-build
soccerwindow2: CMakeFiles/soccerwindow2.dir/build.make

.PHONY : soccerwindow2

# Rule to build all files generated by this target.
CMakeFiles/soccerwindow2.dir/build: soccerwindow2

.PHONY : CMakeFiles/soccerwindow2.dir/build

CMakeFiles/soccerwindow2.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/soccerwindow2.dir/cmake_clean.cmake
.PHONY : CMakeFiles/soccerwindow2.dir/clean

CMakeFiles/soccerwindow2.dir/depend:
	cd /home/leno/gitProjects/HFO_original/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/leno/gitProjects/HFO_original /home/leno/gitProjects/HFO_original /home/leno/gitProjects/HFO_original/build /home/leno/gitProjects/HFO_original/build /home/leno/gitProjects/HFO_original/build/CMakeFiles/soccerwindow2.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/soccerwindow2.dir/depend

