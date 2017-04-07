PROJECT(conanflac)
cmake_minimum_required(VERSION 2.8)
include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

set(LIB_VERSION_MAJOR 1)
set(LIB_VERSION_MINOR 3)
set(LIB_VERSION_PATCH 2)
set(LIB_VERSION ${LIB_VERSION_MAJOR}.${LIB_VERSION_MINOR}.${LIB_VERSION_PATCH})
add_definitions(-DPACKAGE_VERSION="${LIB_VERSION}")

if(MSVC)
    add_definitions(-D_CRT_SECURE_NO_DEPRECATE)
    add_definitions(-D_CRT_NONSTDC_NO_DEPRECATE)
endif()

###############################################################################
# Config.h (replaces config.h.in)
###############################################################################
include(CheckIncludeFiles)
include(CheckFunctionExists)
include(CheckSymbolExists)
include(CheckTypeSize)
include(TestBigEndian)

find_package(Ogg)
if(OGG_FOUND)
    add_definitions(-DFLAC__HAS_OGG=1)
else()
    add_definitions(-DFLAC__HAS_OGG=0)
endif()

find_program(FLAC__HAS_NASM NAMES nasm)
if(FLAC__HAS_NASM)
    add_definitions(-DFLAC__HAS_NASM=1)
else()
    add_definitions(-DFLAC__NO_ASM=1)
endif()

if(NOT MSVC)
    add_definitions(-DFLAC__USE_ALTIVEC=1)
    add_definitions(-DFLAC__USE_AVX=1)
    add_definitions(-DHAVE_CXX_VARARRAYS=1)
    add_definitions(-DHAVE_C_VARARRAYS=1)
endif()

test_big_endian(CPU_IS_BIG_ENDIAN)
if(APPLE)
    add_definitions(-DAC_APPLE_UNIVERSAL_BUILD=1)
    add_definitions(-DFLAC__SYS_DARWIN=1)
elseif(CPU_IS_BIG_ENDIAN)
    add_definitions(-DCPU_IS_BIG_ENDIAN=1)
else()
    add_definitions(-DCPU_IS_LITTLE_ENDIAN=1)
endif()

if(CMAKE_SIZEOF_VOID_P EQUAL "8")
    add_definitions(-DFLAC__ALIGN_MALLOC_DATA=1)
    if(CMAKE_SYSTEM_PROCESSOR STREQUAL "x86_64")
        add_definitions(-DFLAC__CPU_X86_64=1)
    endif()
endif()

if(LINUX)
    add_definitions(-DFLAC__SYS_LINUX=1)
endif()

if(UNIX OR MINGW)
    set(CMAKE_REQUIRED_LIBRARIES m)
    check_function_exists(lround HAVE_LROUND)
    if(HAVE_LROUND)
        add_definitions(-DHAVE_LROUND)
    endif()
endif()

check_function_exists(__builtin_bswap16 HAVE_BSWAP16)
if(HAVE_BSWAP16)
    add_definitions(-DHAVE_BSWAP16)
endif()
check_function_exists(__builtin_bswap32 HAVE_BSWAP32)
if(HAVE_BSWAP32)
    add_definitions(-DHAVE_BSWAP32)
endif()

set(CMAKE_REQUIRED_INCLUDES time.h)
check_function_exists(clock_gettime HAVE_CLOCK_GETTIME)
if(HAVE_CLOCK_GETTIME)
    add_definitions(-DHAVE_CLOCK_GETTIME)
endif()

set(CMAKE_REQUIRED_INCLUDES langinfo.h)
check_function_exists(nl_langinfo HAVE_LANGINFO_CODESET)
if(HAVE_LANGINFO_CODESET)
    add_definitions(-DHAVE_LANGINFO_CODESET=1)
endif()

set(CMAKE_REQUIRED_INCLUDES stdio.h)
check_function_exists(fseeko HAVE_FSEEKO)
if(HAVE_FSEEKO)
    add_definitions(-DHAVE_FSEEKO=1)
endif()

check_function_exists(getopt_long HAVE_GETOPT_LONG)
if(HAVE_GETOPT_LONG)
    add_definitions(-DHAVE_GETOPT_LONG=1)
endif()

check_function_exists(iconv HAVE_ICONV)
if(HAVE_ICONV)
    add_definitions(-DHAVE_ICONV=1)
endif()

set(CMAKE_REQUIRED_INCLUDES sys/socket.h)
check_type_size(socklen_t SOCKLEN_T)
if(HAVE_SOCKLEN_T)
    add_definitions(-DHAVE_SOCKLEN_T=1)
endif()

check_include_files(byteswap.h HAVE_BYTESWAP_H)
if(HAVE_BYTESWAP_H)
    add_definitions(-DHAVE_BYTESWAP_H=1)
endif()
check_include_files(cpuid.h HAVE_CPUID_H)
if(HAVE_CPUID_H)
    add_definitions(-DHAVE_CPUID_H=1)
endif()
check_include_files(dlfcn.h HAVE_DLFCN_H)
if(HAVE_DLFCN_H)
    add_definitions(-DHAVE_DLFCN_H=1)
endif()
check_include_files(inttypes.h HAVE_INTTYPES_H)
if(HAVE_INTTYPES_H)
    add_definitions(-DHAVE_INTTYPES_H=1)
endif()
check_include_files(memory.h HAVE_MEMORY_H)
if(HAVE_MEMORY_H)
    add_definitions(-DHAVE_MEMORY_H=1)
endif()
check_include_files(stdint.h HAVE_STDINT_H)
if(HAVE_STDINT_H)
    add_definitions(-DHAVE_STDINT_H=1)
endif()
check_include_files(stdlib.h HAVE_STDLIB_H)
if(HAVE_STDLIB_H)
    add_definitions(-DHAVE_STDLIB_H=1)
endif()
check_include_files(strings.h HAVE_STRINGS_H)
if(HAVE_STRINGS_H)
    add_definitions(-DHAVE_STRINGS_H=1)
endif()
check_include_files(string.h HAVE_STRING_H)
if(HAVE_STRING_H)
    add_definitions(-DHAVE_STRING_H=1)
endif()
check_include_files(sys/ioctl.h HAVE_SYS_IOCTL_H)
if(HAVE_SYS_IOCTL_H)
    add_definitions(-DHAVE_SYS_IOCTL_H=1)
endif()
check_include_files(sys/param.h HAVE_SYS_PARAM_H)
if(HAVE_SYS_PARAM_H)
    add_definitions(-DHAVE_SYS_PARAM_H=1)
endif()
check_include_files(sys/stat.h HAVE_SYS_STAT_H)
if(HAVE_SYS_STAT_H)
    add_definitions(-DHAVE_SYS_STAT_H=1)
endif()
check_include_files(sys/types.h HAVE_SYS_TYPES_H)
if(HAVE_SYS_TYPES_H)
    add_definitions(-DHAVE_SYS_TYPES_H=1)
endif()
check_include_files(termios.h HAVE_TERMIOS_H)
if(HAVE_TERMIOS_H)
    add_definitions(-DHAVE_TERMIOS_H=1)
endif()
check_include_files(unistd.h HAVE_UNISTD_H)
if(HAVE_UNISTD_H)
    add_definitions(-DHAVE_UNISTD_H=1)
endif()
check_include_files(x86intrin.h HAVE_X86INTRIN_H)
if(HAVE_X86INTRIN_H)
    add_definitions(-DHAVE_X86INTRIN_H=1)
endif()

#configure_file(config.h.in include/config.h @ONLY)
#include_directories(${PROJECT_BINARY_DIR}/include)
#add_definitions(-DHAVE_CONFIG_H)

include_directories(include)

###############################################################################
# List of public library sources
###############################################################################
set(LIB1_NAME FLAC)
set(LIB2_NAME FLAC++)
if(BUILD_SHARED_LIBS)
    if(MSVC)
        set(LIB1_NAME FLAC_dynamic)
        set(LIB2_NAME FLAC++_dynamic)
    endif()
else()
    if(MSVC)
        set(LIB1_NAME FLAC_static)
        set(LIB2_NAME FLAC++_static)
    endif()
    add_definitions(-DFLAC__NO_DLL)
endif()

set(LIB1_PUBLIC_HEADERS
    include/FLAC/all.h
    include/FLAC/assert.h
    include/FLAC/callback.h
    include/FLAC/export.h
    include/FLAC/format.h
    include/FLAC/metadata.h
    include/FLAC/ordinals.h
    include/FLAC/stream_decoder.h
    include/FLAC/stream_encoder.h
)

set(LIB1_SOURCES
    src/libFLAC/bitmath.c
    src/libFLAC/bitreader.c
    src/libFLAC/bitwriter.c
    src/libFLAC/cpu.c
    src/libFLAC/crc.c
    src/libFLAC/fixed.c
    src/libFLAC/fixed_intrin_sse2.c
    src/libFLAC/fixed_intrin_ssse3.c
    src/libFLAC/float.c
    src/libFLAC/format.c
    src/libFLAC/lpc.c
    src/libFLAC/lpc_intrin_avx2.c
    src/libFLAC/lpc_intrin_sse2.c
    src/libFLAC/lpc_intrin_sse41.c
    src/libFLAC/lpc_intrin_sse.c
    src/libFLAC/md5.c
    src/libFLAC/memory.c
    src/libFLAC/metadata_iterators.c
    src/libFLAC/metadata_object.c
    src/libFLAC/stream_decoder.c
    src/libFLAC/stream_encoder.c
    src/libFLAC/stream_encoder_framing.c
    src/libFLAC/stream_encoder_intrin_avx2.c
    src/libFLAC/stream_encoder_intrin_sse2.c
    src/libFLAC/stream_encoder_intrin_ssse3.c
    src/libFLAC/window.c
)
if(OGG_FOUND)
    include_directories(${OGG_INCLUDE_DIRS})
    set(LIB1_SOURCES ${LIB1_SOURCES}
        src/libFLAC/ogg_decoder_aspect.c
        src/libFLAC/ogg_encoder_aspect.c
        src/libFLAC/ogg_helper.c
        src/libFLAC/ogg_mapping.c)
endif()
if(WIN32)
    set(LIB1_SOURCES ${LIB1_SOURCES}
        src/libFLAC/windows_unicode_filenames.c)
endif()

add_library(${LIB1_NAME} ${LIB1_SOURCES})
target_include_directories(${LIB1_NAME} PRIVATE src/libFLAC/include)
if(OGG_FOUND)
    target_link_libraries(${LIB1_NAME} ${OGG_LIBRARIES})
endif()
if(HAVE_LROUND)
    target_link_libraries(${LIB1_NAME} m)
endif()

set(LIB2_PUBLIC_HEADERS
    include/FLAC++/all.h
    include/FLAC++/decoder.h
    include/FLAC++/encoder.h
    include/FLAC++/export.h
    include/FLAC++/metadata.h
)

set(LIB2_SOURCES
    src/libFLAC++/metadata.cpp
    src/libFLAC++/stream_decoder.cpp
    src/libFLAC++/stream_encoder.cpp
)

add_library(${LIB2_NAME} ${LIB2_SOURCES})
if(BUILD_SHARED_LIBS)
    target_link_libraries(${LIB2_NAME} ${LIB1_NAME})
endif()
if(MSVC)
    if(BUILD_SHARED_LIBS)
        target_compile_definitions(${LIB1_NAME} PRIVATE -DFLAC_API_EXPORTS)
        target_compile_definitions(${LIB2_NAME} PRIVATE -DFLACPP_API_EXPORTS)
    endif()
    target_compile_definitions(${LIB1_NAME} PRIVATE -DFLAC__CPU_IA32)
    target_compile_definitions(${LIB1_NAME} PRIVATE -DFLAC__OVERFLOW_DETECT)
endif()
if(OGG_FOUND)
    target_link_libraries(${LIB2_NAME} ${OGG_LIBRARIES})
endif()

set_target_properties(${LIB1_NAME} PROPERTIES SOVERSION ${LIB_VERSION_MAJOR})
set_target_properties(${LIB2_NAME} PROPERTIES SOVERSION ${LIB_VERSION_MAJOR})
if(NOT CYGWIN)
    # This property causes shared libraries on Linux to have the full version
    # encoded into their final filename.  We disable this on Cygwin because
    # it causes cygz-${ZLIB_FULL_VERSION}.dll to be created when cygz.dll
    # seems to be the default.
    set_target_properties(${LIB1_NAME} PROPERTIES VERSION ${LIB_VERSION})
    set_target_properties(${LIB2_NAME} PROPERTIES VERSION ${LIB_VERSION})
endif()

###############################################################################
# Install rules for public libraries and executables
###############################################################################
install(FILES ${LIB1_PUBLIC_HEADERS} DESTINATION include/FLAC)
install(FILES ${LIB2_PUBLIC_HEADERS} DESTINATION include/FLAC++)
install(TARGETS ${LIB1_NAME} ${LIB2_NAME}
        RUNTIME DESTINATION bin
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib)

if(BUILD_SHARED_LIBS)
    set(LIB1_PC ${PROJECT_BINARY_DIR}/flac.pc)
    set(LIB2_PC ${PROJECT_BINARY_DIR}/flac++.pc)
    set(prefix ${CMAKE_INSTALL_PREFIX})
    set(exec_prefix ${CMAKE_INSTALL_PREFIX})
    set(libdir ${CMAKE_INSTALL_PREFIX}/lib)
    set(includedir ${CMAKE_INSTALL_PREFIX}/include)
    set(VERSION ${LIB_VERSION})
    if(OGG_FOUND)
        set(OGG_PACKAGE ogg)
    else()
        set(OGG_PACKAGE )
    endif()
    configure_file(src/libFLAC/flac.pc.in ${LIB1_PC} @ONLY)
    configure_file(src/libFLAC++/flac++.pc.in ${LIB2_PC} @ONLY)
    install(FILES ${LIB1_PC} ${LIB2_PC} DESTINATION lib/pkgconfig)
endif()

