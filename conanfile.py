from conans import CMake, ConanFile, AutoToolsBuildEnvironment, tools
import os
import shutil

class FlacConan(ConanFile):
    name = "FLAC"
    src_name = "flac"
    version = "1.3.2"
    ZIP_FOLDER_NAME = src_name + "-" + version
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    requires = "ogg/1.3.2@GatorQue/stable"
    options = {"shared": [True, False]}
    default_options = "ogg:shared=True", "shared=True"
    exports = ["CMakeLists.txt", "FindFLAC.cmake", "FindFLAC++.cmake"]
    url="http://github.com/GatorQue/conan-flac"
    license="MIT License"
    description="Free Lossless Audio Codec Library"

    def system_requirements(self):
        if self.settings.os == "Linux":
            installer = tools.SystemPackageTool()
            installer.install("xz-utils")
        elif self.settings.os == "Macos":
            installer = tools.SystemPackageTool()
            installer.install("xz")
        elif self.settings.os == "Windows":
            installer = tools.SystemPackageTool()
            installer.install("7zip")

    def source(self):
        zip_name = "%s-%s.tar.xz" % (self.src_name, self.version)
        tools.download("http://downloads.xiph.org/releases/flac/%s" % zip_name, zip_name)
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            self.run("xz -d %s" % zip_name)
            self.run("tar -xf %s" % zip_name.replace(".xz", ""))
        else:
            self.run("7z e %s" % zip_name)
            os.unlink(zip_name)
            self.run("7z x %s" % zip_name.replace(".xz", ""))

        os.unlink(zip_name.replace(".xz", ""))
        if self.settings.os == "Windows":
            shutil.move("CMakeLists.txt", "%s/CMakeLists.txt" % self.ZIP_FOLDER_NAME)

    def build(self):
        if self.settings.os == "Windows":
            cmake = CMake(self.settings)

            cmake_options = []
            cmake_options.append("-DCMAKE_INSTALL_PREFIX:PATH=../install")
            if self.options.shared == True:
                cmake_options.append("-DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=ON")
                cmake_options.append("-DBUILD_SHARED_LIBS=ON")

            self.run("IF not exist build mkdir build")
            cd_build = "cd build"
            self.output.warn('%s && cmake ../%s %s %s' % (cd_build, self.ZIP_FOLDER_NAME, cmake.command_line, " ".join(cmake_options)))
            self.run('%s && cmake ../%s %s %s' % (cd_build, self.ZIP_FOLDER_NAME, cmake.command_line, " ".join(cmake_options)))
            self.output.warn('%s && cmake --build . --target install %s' % (cd_build, cmake.build_config))
            self.run('%s && cmake --build . --target install %s' % (cd_build, cmake.build_config))
        else:
            env_build = AutoToolsBuildEnvironment(self)
            env_build.fpic = self.options.shared

            conf_options = []
            conf_options.append("--prefix=/")
            if self.options.shared == True:
                conf_options.append("--enable-shared")
                conf_options.append("--disable-static")
            else:
                conf_options.append("--disable-shared")
                conf_options.append("--enable-static")

            if self.settings.os == "Macos":
                old_str = '-install_name \$rpath/\$soname'
                new_str = '-install_name \$soname'
                tools.replace_in_file("./%s/configure" % self.ZIP_FOLDER_NAME, old_str, new_str)
                if self.settings.arch == "x86":
                    conf_options.append("--host i686-apple-darwin")
                elif self.settings.arch == "x86_64":
                    conf_options.append("--host x86_64-apple-darwin")

            with tools.environment_append(env_build.vars):
                self.run("./configure %s" % " ".join(conf_options), cwd=self.ZIP_FOLDER_NAME)
                self.run("make", cwd=self.ZIP_FOLDER_NAME)
                self.run("make install DESTDIR=%s/install" % self.conanfile_directory, cwd=self.ZIP_FOLDER_NAME)

    def package(self):
        self.copy("FindFLAC.cmake", dst=".", src=".")
        self.copy("FindFLAC++.cmake", dst=".", src=".")
        self.copy("*", dst="include", src="install/include")
        self.copy("*", dst="lib", src="install/lib", links=True)
        self.copy("*", dst="bin", src="install/bin")

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        if self.settings.os == "Windows":
            if self.options.shared == False:
                self.cpp_info.defines = ["FLAC__NO_DLL", "FLAC__NO_DLL"]
            if self.settings.compiler == "Visual Studio":
                if self.options.shared == True:
                    self.cpp_info.libs = ["FLAC_dynamic","FLAC++_dynamic"]
                else:
                    self.cpp_info.libs = ["FLAC_static","FLAC++_static"]
            else:
                self.cpp_info.libs = ["FLAC", "FLAC++"]
        else:
            self.cpp_info.libs = ["FLAC", "FLAC++"]
