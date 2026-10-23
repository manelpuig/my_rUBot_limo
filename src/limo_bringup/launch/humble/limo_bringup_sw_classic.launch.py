import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    bringup_share = get_package_share_directory("limo_bringup")
    description_share = get_package_share_directory("limo_description")

    world = LaunchConfiguration("world")
    model = LaunchConfiguration("model")
    use_rviz = LaunchConfiguration("use_rviz")
    robot_description = ParameterValue(
        Command(["xacro ", model, " use_gz:=false"]), value_type=str
    )

    state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description, "use_sim_time": True}],
    )
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("gazebo_ros"),
                "launch",
                "gazebo.launch.py",
            )
        ),
        launch_arguments={"world": world}.items(),
    )
    spawn_robot = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        output="screen",
        arguments=[
            "-entity", "limo",
            "-topic", "robot_description",
            "-x", LaunchConfiguration("x"),
            "-y", LaunchConfiguration("y"),
            "-z", LaunchConfiguration("z"),
            "-Y", LaunchConfiguration("yaw"),
        ],
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
                default_value=os.path.join(
                    bringup_share, "worlds", "classic", "empty_world.world"
                ),
            ),
            DeclareLaunchArgument(
                "model",
                default_value=os.path.join(
                    description_share,
                    "urdf",
                    "limo.urdf.xacro",
                ),
            ),
            DeclareLaunchArgument("use_rviz", default_value="true"),
            DeclareLaunchArgument("x", default_value="0.0"),
            DeclareLaunchArgument("y", default_value="0.0"),
            DeclareLaunchArgument("z", default_value="0.10"),
            DeclareLaunchArgument("yaw", default_value="0.0"),
            state_publisher,
            gazebo,
            TimerAction(period=3.0, actions=[spawn_robot]),
            rviz,
        ]
    )
