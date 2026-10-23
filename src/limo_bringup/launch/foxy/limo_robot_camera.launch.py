import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    camera_launch = os.path.join(
        get_package_share_directory("orbbec_camera"), "launch", "dabai.launch.py"
    )

    mount_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="base_to_camera_tf",
        condition=IfCondition(LaunchConfiguration("publish_camera_mount_tf")),
        arguments=[
            LaunchConfiguration("camera_x"),
            LaunchConfiguration("camera_y"),
            LaunchConfiguration("camera_z"),
            LaunchConfiguration("camera_yaw"),
            LaunchConfiguration("camera_pitch"),
            LaunchConfiguration("camera_roll"),
            LaunchConfiguration("base_frame"),
            LaunchConfiguration("camera_frame"),
        ],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("camera_name", default_value="camera"),
            DeclareLaunchArgument("enable_point_cloud", default_value="true"),
            DeclareLaunchArgument("enable_colored_point_cloud", default_value="false"),
            DeclareLaunchArgument("publish_camera_mount_tf", default_value="false"),
            DeclareLaunchArgument("base_frame", default_value="base_link"),
            DeclareLaunchArgument("camera_frame", default_value="camera_link"),
            DeclareLaunchArgument("camera_x", default_value="0.0"),
            DeclareLaunchArgument("camera_y", default_value="0.0"),
            DeclareLaunchArgument("camera_z", default_value="0.0"),
            DeclareLaunchArgument("camera_roll", default_value="0.0"),
            DeclareLaunchArgument("camera_pitch", default_value="0.0"),
            DeclareLaunchArgument("camera_yaw", default_value="0.0"),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(camera_launch),
                launch_arguments={
                    "camera_name": LaunchConfiguration("camera_name"),
                    "color_width": "640",
                    "color_height": "480",
                    "color_fps": "30",
                    "depth_width": "640",
                    "depth_height": "400",
                    "depth_fps": "30",
                    "ir_width": "640",
                    "ir_height": "400",
                    "ir_fps": "30",
                    "enable_point_cloud": LaunchConfiguration("enable_point_cloud"),
                    "enable_colored_point_cloud": LaunchConfiguration(
                        "enable_colored_point_cloud"
                    ),
                }.items(),
            ),
            mount_tf,
        ]
    )
