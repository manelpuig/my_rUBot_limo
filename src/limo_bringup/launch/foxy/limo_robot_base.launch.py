import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    base_launch = os.path.join(
        get_package_share_directory("limo_base"), "launch", "limo_base.launch.py"
    )
    default_model = os.path.join(
        get_package_share_directory("limo_description"), "urdf", "limo.urdf.xacro"
    )

    robot_description = Command(
        [
            "xacro ",
            LaunchConfiguration("model"),
            " use_gz:=true",
            " laser_x:=", LaunchConfiguration("laser_x"),
            " laser_y:=", LaunchConfiguration("laser_y"),
            " laser_z:=", LaunchConfiguration("laser_z"),
            " laser_roll:=", LaunchConfiguration("laser_roll"),
            " laser_pitch:=", LaunchConfiguration("laser_pitch"),
            " laser_yaw:=", LaunchConfiguration("laser_yaw"),
            " camera_x:=", LaunchConfiguration("camera_x"),
            " camera_y:=", LaunchConfiguration("camera_y"),
            " camera_z:=", LaunchConfiguration("camera_z"),
            " camera_roll:=", LaunchConfiguration("camera_roll"),
            " camera_pitch:=", LaunchConfiguration("camera_pitch"),
            " camera_yaw:=", LaunchConfiguration("camera_yaw"),
        ]
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("port_name", default_value="ttyTHS0"),
            DeclareLaunchArgument("odom_frame", default_value="odom"),
            DeclareLaunchArgument("base_frame", default_value="base_footprint"),
            DeclareLaunchArgument("publish_odom_tf", default_value="true"),
            DeclareLaunchArgument("use_mecanum", default_value="true"),
            DeclareLaunchArgument("model", default_value=default_model),
            DeclareLaunchArgument("laser_x", default_value="0.103"),
            DeclareLaunchArgument("laser_y", default_value="0.0"),
            DeclareLaunchArgument("laser_z", default_value="-0.034"),
            DeclareLaunchArgument("laser_roll", default_value="0.0"),
            DeclareLaunchArgument("laser_pitch", default_value="0.0"),
            DeclareLaunchArgument("laser_yaw", default_value="0.0"),
            DeclareLaunchArgument("camera_x", default_value="0.084"),
            DeclareLaunchArgument("camera_y", default_value="0.0"),
            DeclareLaunchArgument("camera_z", default_value="0.03"),
            DeclareLaunchArgument("camera_roll", default_value="0.0"),
            DeclareLaunchArgument("camera_pitch", default_value="0.0"),
            DeclareLaunchArgument("camera_yaw", default_value="0.0"),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="limo_robot_state_publisher",
                output="screen",
                parameters=[{"robot_description": robot_description}],
            ),
            Node(
                package="joint_state_publisher",
                executable="joint_state_publisher",
                name="limo_joint_state_publisher",
                output="screen",
                parameters=[{"robot_description": robot_description}],
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(base_launch),
                launch_arguments={
                    "port_name": LaunchConfiguration("port_name"),
                    "odom_frame": LaunchConfiguration("odom_frame"),
                    "base_frame": LaunchConfiguration("base_frame"),
                    "pub_odom_tf": LaunchConfiguration("publish_odom_tf"),
                    "pub_imu_tf": "false",
                    "use_mecanum": LaunchConfiguration("use_mecanum"),
                }.items(),
            ),
        ]
    )
