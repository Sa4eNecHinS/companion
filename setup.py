from setuptools import find_packages, setup
from pathlib import Path

package_name = "lwitch"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(include=["lwitch", "lwitch.*"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=[
        "numpy",
        "openai",
        "faster-whisper",
        "sounddevice",
        "wavio",
        "python-dotenv",
        "SQLAlchemy>=2,<3",
        "psycopg2-binary",
    ],
    zip_safe=True,
    python_requires=">=3.10",
    maintainer="Sa4eNecHinS",
    maintainer_email="root@todo.todo",
    description="Companion: experimental ROS 2 voice assistant",
    long_description=Path(__file__).with_name("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/Sa4eNecHinS/companion",
    license="Apache-2.0",
    extras_require={
        "vad": ["silero-vad"],
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "stt_node = lwitch.nodes.stt_node:main",
            "voice_input = lwitch.nodes.voice_input_node:main",
            "input_node = lwitch.nodes.input_node:main",
            "waf_filter = lwitch.nodes.waf_filter_node:main",
        ],
    },
)
