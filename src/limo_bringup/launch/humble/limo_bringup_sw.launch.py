import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
    TimerAction,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, EnvironmentVariable, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    bringup_share = get_package_share_directory("limo_bringup")
    description_share = get_package_share_directory("limo_description")
    ros_gz_share = get_package_share_directory("ros_gz_sim")

    world = LaunchConfiguration("world")
    model = LaunchConfiguration("model")
    robot_name = LaunchConfiguration("robot_name")
    use_rviz = LaunchConfiguration("use_rviz")
    x = LaunchConfiguration("x")
    y = LaunchConfiguration("y")
    z = LaunchConfiguration("z")
    yaw = LaunchConfiguration("yaw")

    robot_description = ParameterValue(Command(["xacro ", model]), value_type=str)

    state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description, "use_sim_time": True}],
    )
    joint_state_publisher = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        output="screen",
        parameters=[{"use_sim_time": True}],
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_share, "launch", "gz_sim.launch.py")
        ),
        launch_arguments={"gz_args": ["-r ", world]}.items(),
    )
    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=[
            "-name", robot_name,
            "-topic", "robot_description",
            "-x", x,
            "-y", y,
            "-z", z,
            "-Y", yaw,
        ],
    )
    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="limo_ros_gz_bridge",
        output="screen",
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock",
            "/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist",
            "/odom@nav_msgs/msg/Odometry[ignition.msgs.Odometry",
            "/scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan",
            "/imu@sensor_msgs/msg/Imu[ignition.msgs.IMU",
            "/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V",
            "/camera/color@sensor_msgs/msg/Image[ignition.msgs.Image",
            "/camera/color/camera_info@sensor_msgs/msg/CameraInfo[ignition.msgs.CameraInfo",
            "--ros-args",
            "-r", "/camera/color:=/camera/color/image_raw",
        ],
        parameters=[{"use_sim_time": True}],
    )
    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", os.path.join(bringup_share, "rviz", "limo_simulation.rviz")],
        parameters=[{"use_sim_time": True}],
        condition=IfCondition(use_rviz),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "world",
                default_value=os.path.join(bringup_share, "worlds", "empty_world.sdf"),
            ),
            DeclareLaunchArgument(
                "model",
                default_value=os.path.join(
                    description_share, "urdf", "limo.urdf.xacro"
                ),
            ),
            DeclareLaunchArgument("robot_name", default_value="limo"),
            DeclareLaunchArgument("use_rviz", default_value="true"),
            DeclareLaunchArgument("x", default_value="0.0"),
            DeclareLaunchArgument("y", default_value="0.0"),
            DeclareLaunchArgument("z", default_value="0.16"),
            DeclareLaunchArgument("yaw", default_value="0.0"),
            SetEnvironmentVariable(
                "IGN_GAZEBO_RESOURCE_PATH",
                [
                    description_share,
                    os.pathsep,
                    bringup_share,
                    os.pathsep,
                    EnvironmentVariable("IGN_GAZEBO_RESOURCE_PATH", default_value=""),
                ],
            ),
            SetEnvironmentVariable(
                "GZ_SIM_RESOURCE_PATH",
                [
                    description_share,
                    os.pathsep,
                    bringup_share,
                    os.pathsep,
                    EnvironmentVariable("GZ_SIM_RESOURCE_PATH", default_value=""),
                ],
            ),
            state_publisher,
            joint_state_publisher,
            gazebo,
            TimerAction(period=3.0, actions=[spawn_robot, bridge]),
            rviz,
        ]
    )
