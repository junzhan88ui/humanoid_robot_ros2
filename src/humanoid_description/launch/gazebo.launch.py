import os
import xacro

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription

from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    pkg_name = "humanoid_description"

    pkg_share = get_package_share_directory(pkg_name)

    xacro_file = os.path.join(
        pkg_share,
        "urdf",
        "humanoid.xacro"
    )


    robot_description = {
        "robot_description":
            xacro.process_file(
                xacro_file
            ).toxml()
    }


    # Gazebo Sim
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory(
                    "ros_gz_sim"
                ),
                "launch",
                "gz_sim.launch.py"
            )
        ),
        launch_arguments={
            "gz_args": "-r empty.sdf"
        }.items()
    )


    # Publish robot description and TF
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[
            robot_description
        ],
        output="screen"
    )


    # Spawn humanoid into Gazebo
    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-name",
            "humanoid",
            "-topic",
            "robot_description"
        ],
        output="screen"
    )


    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot,
    ])

