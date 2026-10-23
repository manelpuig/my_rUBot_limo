import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    bringup_share = get_package_share_directory("limo_bringup")
    foxy_launch_dir = os.path.join(bringup_share, "launch", "foxy")

    base = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(foxy_launch_dir, "limo_robot_base.launch.py")
        ),
        launch_arguments={
            "port_name": LaunchConfiguration("base_port"),
            "publish_odom_tf": LaunchConfiguration("publish_odom_tf"),
            "use_mecanum": LaunchConfiguration("use_mecanum"),
            "laser_x": LaunchConfiguration("laser_x"),
            "laser_y": LaunchConfiguration("laser_y"),
            "laser_z": LaunchConfiguration("laser_z"),
            "laser_roll": LaunchConfiguration("laser_roll"),
            "laser_pitch": LaunchConfiguration("laser_pitch"),
            "laser_yaw": LaunchConfiguration("laser_yaw"),
            "camera_x": LaunchConfiguration("camera_x"),
            "camera_y": LaunchConfiguration("camera_y"),
            "camera_z": LaunchConfiguration("camera_z"),
            "camera_roll": LaunchConfiguration("camera_roll"),
            "camera_pitch": LaunchConfiguration("camera_pitch"),
            "camera_yaw": LaunchConfiguration("camera_yaw"),
        }.items(),
    )

    lidar = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(foxy_launch_dir, "limo_robot_lidar.launch.py")
        ),
        condition=IfCondition(LaunchConfiguration("use_lidar")),
        launch_arguments={
            "params_file": LaunchConfiguration("lidar_params_file"),
            "laser_x": LaunchConfiguration("laser_x"),
            "laser_y": LaunchConfiguration("laser_y"),
            "laser_z": LaunchConfiguration("laser_z"),
            "laser_roll": LaunchConfiguration("laser_roll"),
            "laser_pitch": LaunchConfiguration("laser_pitch"),
            "laser_yaw": LaunchConfiguration("laser_yaw"),
            "publish_lidar_tf": "false",
        }.items(),
    )

    camera = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(foxy_launch_dir, "limo_robot_camera.launch.py")
        ),
        condition=IfCondition(LaunchConfiguration("use_camera")),
        launch_arguments={
            "enable_point_cloud": LaunchConfiguration("enable_point_cloud"),
            "publish_camera_mount_tf": "false",
        }.items(),
    )

    rf2o_launch = os.path.join(
        get_package_share_directory("rf2o_laser_odometry"),
        "launch",
        "rf2o_laser_odometry.launch.py",
    )
    rf2o = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(rf2o_launch),
        condition=IfCondition(LaunchConfiguration("use_rf2o")),
        launch_arguments={
            "odom_topic": "/rf2o/odom",
            "publish_tf": "false",
        }.items(),
    )

    default_lidar_params = os.path.join(
        get_package_share_directory("ydlidar_ros2_driver"), "params", "ydlidar.yaml"
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("base_port", default_value="ttyTHS0"),
            DeclareLaunchArgument("use_mecanum", default_value="true"),
            DeclareLaunchArgument("publish_odom_tf", default_value="true"),
            DeclareLaunchArgument("use_lidar", default_value="true"),
            DeclareLaunchArgument("use_camera", default_value="true"),
            DeclareLaunchArgument("use_rf2o", default_value="false"),
            DeclareLaunchArgument("lidar_params_file", default_value=default_lidar_params),
            DeclareLaunchArgument("laser_x", default_value="0.103"),
            DeclareLaunchArgument("laser_y", default_value="0.0"),
            DeclareLaunchArgument(
                "laser_z",
                default_value="0.02",
                description="Measure this LIMO Pro installation before release.",
            ),
            DeclareLaunchArgument("laser_roll", default_value="0.0"),
            DeclareLaunchArgument("laser_pitch", default_value="0.0"),
            DeclareLaunchArgument("laser_yaw", default_value="0.0"),
            DeclareLaunchArgument("enable_point_cloud", default_value="true"),
            DeclareLaunchArgument("camera_x", default_value="0.084"),
            DeclareLaunchArgument("camera_y", default_value="0.0"),
            DeclareLaunchArgument("camera_z", default_value="0.03"),
            DeclareLaunchArgument("camera_roll", default_value="0.0"),
            DeclareLaunchArgument("camera_pitch", default_value="0.0"),
            DeclareLaunchArgument("camera_yaw", default_value="0.0"),
            base,
            lidar,
            camera,
            TimerAction(period=5.0, actions=[rf2o]),
        ]
    )
