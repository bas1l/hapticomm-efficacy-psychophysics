# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.18

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Disable VCS-based implicit rules.
% : %,v


# Disable VCS-based implicit rules.
% : RCS/%


# Disable VCS-based implicit rules.
% : RCS/%,v


# Disable VCS-based implicit rules.
% : SCCS/s.%


# Disable VCS-based implicit rules.
% : s.%


.SUFFIXES: .hpux_make_needs_suffix_list


# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
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
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/pi/Software/hapticomm-efficacy-psychophysics/hapticommlib

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/pi/Software/hapticomm-efficacy-psychophysics/build

# Include any dependencies generated for this target.
include CMakeFiles/HaptiCommConfiguration.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/HaptiCommConfiguration.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/HaptiCommConfiguration.dir/flags.make

CMakeFiles/HaptiCommConfiguration.dir/2_src/HaptiCommConfiguration.cpp.o: CMakeFiles/HaptiCommConfiguration.dir/flags.make
CMakeFiles/HaptiCommConfiguration.dir/2_src/HaptiCommConfiguration.cpp.o: /home/pi/Software/hapticomm-efficacy-psychophysics/hapticommlib/2_src/HaptiCommConfiguration.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/pi/Software/hapticomm-efficacy-psychophysics/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/HaptiCommConfiguration.dir/2_src/HaptiCommConfiguration.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/HaptiCommConfiguration.dir/2_src/HaptiCommConfiguration.cpp.o -c /home/pi/Software/hapticomm-efficacy-psychophysics/hapticommlib/2_src/HaptiCommConfiguration.cpp

CMakeFiles/HaptiCommConfiguration.dir/2_src/HaptiCommConfiguration.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/HaptiCommConfiguration.dir/2_src/HaptiCommConfiguration.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/pi/Software/hapticomm-efficacy-psychophysics/hapticommlib/2_src/HaptiCommConfiguration.cpp > CMakeFiles/HaptiCommConfiguration.dir/2_src/HaptiCommConfiguration.cpp.i

CMakeFiles/HaptiCommConfiguration.dir/2_src/HaptiCommConfiguration.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/HaptiCommConfiguration.dir/2_src/HaptiCommConfiguration.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/pi/Software/hapticomm-efficacy-psychophysics/hapticommlib/2_src/HaptiCommConfiguration.cpp -o CMakeFiles/HaptiCommConfiguration.dir/2_src/HaptiCommConfiguration.cpp.s

# Object files for target HaptiCommConfiguration
HaptiCommConfiguration_OBJECTS = \
"CMakeFiles/HaptiCommConfiguration.dir/2_src/HaptiCommConfiguration.cpp.o"

# External object files for target HaptiCommConfiguration
HaptiCommConfiguration_EXTERNAL_OBJECTS =

libHaptiCommConfiguration.a: CMakeFiles/HaptiCommConfiguration.dir/2_src/HaptiCommConfiguration.cpp.o
libHaptiCommConfiguration.a: CMakeFiles/HaptiCommConfiguration.dir/build.make
libHaptiCommConfiguration.a: CMakeFiles/HaptiCommConfiguration.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/pi/Software/hapticomm-efficacy-psychophysics/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX static library libHaptiCommConfiguration.a"
	$(CMAKE_COMMAND) -P CMakeFiles/HaptiCommConfiguration.dir/cmake_clean_target.cmake
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/HaptiCommConfiguration.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/HaptiCommConfiguration.dir/build: libHaptiCommConfiguration.a

.PHONY : CMakeFiles/HaptiCommConfiguration.dir/build

CMakeFiles/HaptiCommConfiguration.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/HaptiCommConfiguration.dir/cmake_clean.cmake
.PHONY : CMakeFiles/HaptiCommConfiguration.dir/clean

CMakeFiles/HaptiCommConfiguration.dir/depend:
	cd /home/pi/Software/hapticomm-efficacy-psychophysics/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/pi/Software/hapticomm-efficacy-psychophysics/hapticommlib /home/pi/Software/hapticomm-efficacy-psychophysics/hapticommlib /home/pi/Software/hapticomm-efficacy-psychophysics/build /home/pi/Software/hapticomm-efficacy-psychophysics/build /home/pi/Software/hapticomm-efficacy-psychophysics/build/CMakeFiles/HaptiCommConfiguration.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/HaptiCommConfiguration.dir/depend
