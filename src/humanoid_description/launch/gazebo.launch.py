import os

import xacro

from launch import LaunchDescription

from launch.actions import (
    IncludeLaunchDescription,
    RegisterEventHandler,
)

from launch.event_handlers import (
    OnProcessStart,
    OnProcessExit,
)

from launch.launch_description_sources import (
    PythonLaunchDescriptionSource,
)

from launch_ros.actions import Node

from ament_index_python.packages import (
    get_package_share_directory,
)


def generate_launch_description():

    package_name = "humanoid_description"

    pkg_path = get_package_share_directory(package_name)


    # ==================================================
    # Generate robot_description from xacro
    # ==================================================

    xacro_file = os.path.join(
        pkg_path,
        "urdf",
        "humanoid.xacro"
    )


    robot_description_xml = xacro.process_file(
        xacro_file
    ).toxml()


    robot_description = {

        "robot_description": robot_description_xml

    }


    # ==================================================
    # Gazebo Harmonic
    # ==================================================

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

            "gz_args":
            "-r empty.sdf"

        }.items()

    )


    # ==================================================
    # robot_state_publisher
    # ==================================================

    robot_state_publisher = Node(

        package="robot_state_publisher",

        executable="robot_state_publisher",

        name="robot_state_publisher",

        output="screen",

        parameters=[

            robot_description,

            {
                "use_sim_time": True
            }

        ]

    )


    # ==================================================
    # Spawn robot into Gazebo
    # ==================================================

    spawn_robot = Node(

        package="ros_gz_sim",

        executable="create",

        arguments=[

            "-topic",

            "robot_description",

            "-name",

            "humanoid"

        ],

        output="screen"

    )


    # ==================================================
    # Controller yaml
    # ==================================================

    controller_yaml = os.path.join(

        pkg_path,

        "config",

        "humanoid_controllers.yaml"

    )


    # ==================================================
    # joint_state_broadcaster
    # ==================================================

    joint_state_broadcaster = Node(

        package="controller_manager",

        executable="spawner",

        arguments=[

            "joint_state_broadcaster",

            "--controller-manager",

            "/controller_manager",

            "--param-file",

            controller_yaml

        ],

        output="screen"

    )


    # ==================================================
    # humanoid_controller
    # ==================================================

    humanoid_controller = Node(

        package="controller_manager",

        executable="spawner",

        arguments=[

            "humanoid_controller",

            "--controller-manager",

            "/controller_manager",

            "--param-file",

            controller_yaml

        ],

        output="screen"

    )


    # ==================================================
    # Launch order
    #
    # Gazebo
    #
    # robot_state_publisher
    #
    # spawn robot
    #
    # joint_state_broadcaster
    #
    # humanoid_controller
    #
    # ==================================================


    return LaunchDescription([


        gazebo,


        robot_state_publisher,


        spawn_robot,


        RegisterEventHandler(

            OnProcessExit(

                target_action=spawn_robot,

                on_exit=[

                    joint_state_broadcaster

                ]

            )

        ),


        RegisterEventHandler(

            OnProcessExit(

                target_action=joint_state_broadcaster,

                on_exit=[

                    humanoid_controller

                ]

            )

        )


    ])
