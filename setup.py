from setuptools import find_packages, setup

package_name = "lwitch"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/srv", ["srv/CheckSafety.srv"]),
    ],
    install_requires=[
        "setuptools",
        "openai",
        "faster-whisper",
        "sounddevice",
        "wavio",
        "ctranslate2",
        "dotenv",
    ],
    zip_safe=True,
    maintainer="root",
    maintainer_email="root@todo.todo",
    description="lwitch package",
    license="Apache-2.0",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "stt_node = lwitch.stt.stt_node:main",
            "voice_input = lwitch.stt.voice_input_node:main",
            "llm_response = lwitch.llm.llm_client_node:main",
        ],
    },
)
