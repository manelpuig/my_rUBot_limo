import os
from glob import glob

from setuptools import find_packages, setup


package_name = "limo_nav_control"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
    ],
    install_requires=["setuptools", "PyYAML"],
    zip_safe=True,
    maintainer="Manel Puig",
    maintainer_email="manelpuig@todo.todo",
    description="Waypoint mission control for Nav2 on the LIMO Pro.",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "waypoint_mission = limo_nav_control.waypoint_mission:main",
        ],
    },
)
