import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    default_params = os.path.join(
        get_package_share_directory("limo_yolo"), "config", "yolo11.yaml"
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("params_file", default_value=default_params),
            DeclareLaunchArgument(
                "image_topic", default_value="/camera/color/image_raw"
            ),
            DeclareLaunchArgument("model", default_value="yolo11n.pt"),
            DeclareLaunchArgument("device", default_value="cpu"),
            Node(
                package="limo_yolo",
                executable="yolo_detector",
                name="yolo_detector",
                output="screen",
                parameters=[
                    LaunchConfiguration("params_file"),
                    {
                        "image_topic": LaunchConfiguration("image_topic"),
                        "model": LaunchConfiguration("model"),
                        "device": LaunchConfiguration("device"),
                    },
                ],
            ),
        ]
    )
