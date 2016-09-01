from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager(
        username="laohyx", channel="testing",
        visual_versions=["12"],
        visual_runtimes=["MD", "MDd"]
    )
    builder.add_common_builds(shared_option_name="ZMQ:shared")
    builder.run()
