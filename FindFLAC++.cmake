#.rst:
# FindFlac++
# --------
#
# Find flac++
#
# Find the flac++ libraries
#
# ::
#
#   This module defines the following variables:
#      FLAC++_FOUND       - True if FLAC++_INCLUDE_DIR & FLAC++_LIBRARY are found
#      FLAC++_LIBRARIES   - The FLAC++ library and any linker dependencies
#      FLAC++_DEFINITIONS - Required FLAC++ library import definitions
#      FLAC++_INCLUDE_DIRS - Set when FLAC++_INCLUDE_DIR is found
#
# ::
#
#      FLAC++_INCLUDE_DIR - where to find FLAC++/all.h, etc.
#      FLAC++_LIBRARY     - the asound library

find_package(FLAC REQUIRED)

if(UNIX)
    find_library(FLAC++_MATH_LIBRARY m)
    set(FLAC++_PLATFORM_DEPENDENT_LIBS ${FLAC++_MATH_LIBRARY})
endif()

find_path(FLAC++_INCLUDE_DIR NAMES FLAC++/all.h
          DOC "The FLAC++ include directory"
)

find_library(FLAC++_LIBRARY NAMES FLAC++ FLAC++_dynamic FLAC++_static
          DOC "The FLAC++ library"
)

# handle the QUIETLY and REQUIRED arguments and set FLAC_FOUND to TRUE if
# all listed variables are TRUE
include(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(FLAC++
                                  REQUIRED_VARS FLAC++_LIBRARY FLAC++_INCLUDE_DIR)

if(FLAC++_FOUND)
  set(FLAC++_DEFINITIONS ${FLAC_DEFINITIONS})
  set(FLAC++_LIBRARIES ${FLAC++_LIBRARY} ${FLAC_LIBRARIES} ${FLAC++_PLATFORM_DEPENDENT_LIBS})
  set(FLAC++_INCLUDE_DIRS ${FLAC++_INCLUDE_DIR})
endif()

mark_as_advanced(FLAC++_INCLUDE_DIR FLAC++_LIBRARY)
