import os
from glob import glob

from setuptools import find_packages, setup


package_name = "limo_yolo"


setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        (
            "share/ament_index/resource_index/packages",
            ["resource/" + package_name],
        ),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Manel Puig",
    maintainer_email="manelpuig@todo.todo",
    description="YOLO11 detection from a ROS 2 image topic.",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "yolo_detector = limo_yolo.yolo_detector:main",
        ],
    },
)
