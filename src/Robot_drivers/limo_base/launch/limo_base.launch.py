import launch
import launch_ros

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    port_name_arg = DeclareLaunchArgument(
        "port_name",
        default_value="ttyTHS0",
        description="Serial port name, e.g. ttyTHS0",
    )

    odom_frame_arg = DeclareLaunchArgument(
        "odom_frame",
        default_value="odom",
        description="Odometry frame id",
    )

    base_frame_arg = DeclareLaunchArgument(
        "base_frame",
        default_value="base_link",
        description="Base link frame id",
    )

    pub_odom_tf_arg = DeclareLaunchArgument(
        "pub_odom_tf",
        default_value="true",
        description="Publish odom TF",
    )

    use_mecanum_arg = DeclareLaunchArgument(
        "use_mecanum",
        default_value="true",
        description="Force the LIMO base to use Mecanum kinematics",
    )

    port_name = LaunchConfiguration("port_name")
    odom_frame = LaunchConfiguration("odom_frame")
    base_frame = LaunchConfiguration("base_frame")
    pub_odom_tf = LaunchConfiguration("pub_odom_tf")
    use_mecanum = LaunchConfiguration("use_mecanum")

    limo_base_node = Node(
        package="limo_base",
        executable="limo_base",
        output="screen",
        name="limo_base_node",
        emulate_tty=True,
        parameters=[
            {
                "port_name": port_name,
                "odom_frame": odom_frame,
                "base_frame": base_frame,
                "pub_odom_tf": pub_odom_tf,
                "use_mecanum": use_mecanum,
            }
        ],
        remappings=[
            ("odom", "/wheel/odom"),
        ],
    )

    return LaunchDescription(
        [
            port_name_arg,
            odom_frame_arg,
            base_frame_arg,
            pub_odom_tf_arg,
            use_mecanum_arg,
            limo_base_node,
        ]
    )
