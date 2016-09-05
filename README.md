# conan-opencv
(Forked from https://github.com/memsharded/conan-opencv)

OpenCV computer vision package for conan package manager.

This repository maintains OpenCV 3.1+.

The package is still not uploaded, but working in:
- Win10, MSVC12, Release/Debug, STATIC opencv
- Win10, MSVC14, Release, SHARED opencv
- Third parties libs (zlib, etc), from the bundled source in OpenCV, not using other conan packages (yet)


Steps: 

```bash
$ git clone https://github.com/laohyx/conan-opencv.git
$ cd conan-opencv
$ conan export lhtracking/stable
$ conan test_package
//for other conan defaults
$ conan test_package -s compiler="Visual Studio" -s compiler.version=14 -s arch=x86_64 -s build_type=Release -s compiler.runtime=MD
//to select shared opencv (can combine with above compiler settings)
$ conan test_package -o OpenCV:shared=True
```

Conan re-builds the package with ``conan test_package``, if you want to re-run the test only, you can

```bash
$ conan test_package --build=never (--build=missing will also do it)
```


This is ongoing work:

- Feel free to add tests to build, specially if something fails, with a PR, so the package is better tested
- Report any issues, even if you want to try in different OS, I will add Linux support soon.

