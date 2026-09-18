from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

import os



def generate_launch_description():


    pkg_name = "humanoid_description"


    urdf_file = os.path.join(
        get_package_share_directory(pkg_name),
        "urdf",
        "humanoid.xacro"
    )


    controllers_file = os.path.join(
        get_package_share_directory(pkg_name),
        "config",
        "humanoid_controllers.yaml"
    )



    robot_description = Command(
        [
            "xacro ",
            urdf_file
        ]
    )



    robot_state_publisher = Node(

        package="robot_state_publisher",

        executable="robot_state_publisher",

        name="robot_state_publisher",

        output="screen",

        parameters=[
            {
                "robot_description": robot_description
            }
        ]

    )



    ros2_control_node = Node(

        package="controller_manager",

        executable="ros2_control_node",

        parameters=[

            {
                "robot_description": robot_description
            },

            controllers_file

        ],

        output="screen"

    )



    joint_state_broadcaster = Node(

        package="controller_manager",

        executable="spawner",

        arguments=[

            "joint_state_broadcaster",

            "--controller-manager",

            "/controller_manager",

            "--controller-manager-timeout",

            "30"

        ],

        output="screen"

    )



    humanoid_controller = Node(

        package="controller_manager",

        executable="spawner",

        arguments=[

            "humanoid_controller",

            "--controller-manager",

            "/controller_manager",

            "--controller-manager-timeout",

            "30"


        ],

        output="screen"

    )



    return LaunchDescription([


        robot_state_publisher,


        ros2_control_node,


        joint_state_broadcaster,


        humanoid_controller


    ])
