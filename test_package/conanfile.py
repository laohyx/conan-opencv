from conans import ConanFile, CMake
import os

username = os.getenv("CONAN_USERNAME", "lhtracking")
channel = os.getenv("CONAN_CHANNEL", "stable")

class OpenCVTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "OpenCV/3.1.0@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy("*.dll", "bin", "bin")
        self.copy("*.dylib", "bin", "lib")
        self.copy("haarcascade*.xml", "bin", "data")

    def test(self):
        os.chdir("bin")
        self.run(".%slena" % os.sep)
