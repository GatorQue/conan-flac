#.rst:
# FindFLAC
# --------
#
# Find FLAC
#
# Find the flac libraries
#
# ::
#
#   This module defines the following variables:
#      FLAC_FOUND       - True if FLAC_INCLUDE_DIR & FLAC_LIBRARY are found
#      FLAC_LIBRARIES   - The FLAC library and any linker dependencies
#      FLAC_DEFINITIONS - Required FLAC library import definitions
#      FLAC_INCLUDE_DIRS - Set when FLAC_INCLUDE_DIR is found
#
# ::
#
#      FLAC_INCLUDE_DIR - where to find FLAC/all.h, etc.
#      FLAC_LIBRARY     - the FLAC library

find_package(Ogg)

if(UNIX)
    find_library(FLAC_MATH_LIBRARY m)
    set(FLAC_PLATFORM_DEPENDENT_LIBS ${FLAC_MATH_LIBRARY})
endif()

find_path(FLAC_INCLUDE_DIR NAMES FLAC/all.h
          DOC "The FLAC include directory"
)

find_library(FLAC_LIBRARY NAMES FLAC FLAC_dynamic FLAC_static
          DOC "The FLAC library"
)

# handle the QUIETLY and REQUIRED arguments and set FLAC_FOUND to TRUE if
# all listed variables are TRUE
include(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(FLAC
                                  REQUIRED_VARS FLAC_LIBRARY FLAC_INCLUDE_DIR)

if(FLAC_FOUND)
  get_filename_component(FLAC_LIBRARY_NAME ${FLAC_LIBRARY} NAME_WE)
  if(WIN32 AND FLAC_LIBRARY_NAME MATCHES "_static")
    set(FLAC_DEFINITIONS -DFLAC__NO_DLL)
  else()
    set(FLAC_DEFINITIONS )
  endif()
  unset(FLAC_LIBRARY_NAME)
  set(FLAC_LIBRARIES ${FLAC_LIBRARY} ${OGG_LIBRARIES} ${FLAC_PLATFORM_DEPENDENT_LIBS})
  set(FLAC_INCLUDE_DIRS ${FLAC_INCLUDE_DIR})
endif()

mark_as_advanced(FLAC_INCLUDE_DIR FLAC_LIBRARY)
