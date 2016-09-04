from conans import ConanFile, CMake, tools
import os


class OpenCVConan(ConanFile):
    name = "OpenCV"
    version = "3.1.0"
    license = "LGPL"
    url = "https://github.com/opencv/opencv/archive/3.1.0.zip"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    opencv_modules = ["calib3d", "core", "features2d", "flann", "highgui", "imgcodecs", "imgproc", "ml",
                    "objdetect", "photo", "shape", "stitching", "superres", "video", "videoio", "videostab"]
    def source(self):
        #tools.download("http://localhost:8000/opencv-3.1.0.zip", "opencv.zip")
        tools.download("https://github.com/opencv/opencv/archive/3.1.0.zip", "opencv.zip")

        tools.unzip("opencv.zip")
        os.unlink("opencv.zip")
     
    def build(self):
        cmake = CMake(self.settings)
        try:  # Just convenient for me, if rebuilding (due to cmake bug)
            shutil.rmtree("build", ignore_errors=True)
        except:
            pass
        try:
            os.makedirs("build")
        except:
            pass
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else "-DBUILD_SHARED_LIBS=OFF"
        cmake_flags = ("%s -DBUILD_EXAMPLES=OFF -DBUILD_DOCS=OFF -DBUILD_TESTS=OFF -DBUILD_opencv_apps=OFF -DBUILD_PERF_TESTS=OFF -DWITH_IPP=OFF -DWITH_TBB=OFF"
                        % (shared) )
        if self.settings.compiler == "Visual Studio":
            cmake_flags +=  " -DBUILD_WITH_STATIC_CRT=ON" if "MT" in str(self.settings.compiler.runtime) else " -DBUILD_WITH_STATIC_CRT=OFF"
        print "CMAKE FLAGS ", cmake_flags
        self.run('cd build && cmake ../opencv-%s %s %s' % (self.version, cmake_flags, cmake.command_line))
        self.run("cd build && cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h*", "include", "opencv-%s/include" % self.version)
        for lib in self.opencv_modules:
            self.copy("*.h*", "include", "opencv-%s/modules/%s/include" % (self.version, lib))
        self.copy("*.lib", "lib", "build/lib", keep_path=False)
        self.copy("*.pdb", "lib", "build/lib", keep_path=False) # windows debug info
        self.copy("*.a", "lib", "build/lib", keep_path=False) 
        self.copy("*.dll", "bin", "build/bin", keep_path=False)
        self.copy("*.dylib", "lib", "build/lib", keep_path=False)
        self.copy("*.so", "lib", "build/lib", keep_path=False)
        self.copy("*.xml", "data", "opencv-%s/data" % (self.version))
        
        if not self.options.shared:
            self.copy("*.lib", "lib", "build/3rdparty/lib", keep_path=False)

    def package_info(self):
        for lib in self.opencv_modules:
            self.cpp_info.libs.append("opencv_%s%s%s" % (lib, self.version.replace(".", ""),
                "d" if self.settings.build_type == "Debug" else ""))
        if self.settings.os == "Windows" and not self.options.shared:
            # third party
            for lib in ["IlmImf", "libjasper", "libjpeg", "libpng", "libtiff", "libwebp", "zlib"]:
                self.cpp_info.libs.append("%s%s" % (lib,
                    "d" if self.settings.build_type == "Debug" else ""))
                    
