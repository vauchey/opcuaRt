import launch
import launch_ros.actions

def generate_launch_description():
    ld = launch.LaunchDescription()

    node1=launch_ros.actions.Node(
            package='colibry_communicator',
            executable='robot_sender',
            parameters=[
            {'robot_sender_FREQUENCY': 10},
            {'robot_sender_robotName': "Fab1(MIR)"},
            {'robot_sender_ENCRYPT': 1},
            #{'robot_sender_url': "opc.tcp://127.0.0.1:4840/freeopcua/server/"},
            {'robot_sender_url': "opc.tcp://esigelec.ddns.net:11111/freeopcua/server/"},
            #{'robot_sender_url': "opc.tcp://192.168.2.105:4840/freeopcua/server/"},
            {'robot_sender_namespace': "http://esigelec.ddns.net"},
            #{'robot_sender_certificate': "vincent/my_cert.der"},
            #{'robot_sender_private_key': "vincent/my_private_key.pem"},
            {'robot_sender_certificate': "/home/user/colibry/opcuaRt/MIR1/my_cert.der"},
            {'robot_sender_private_key': "/home/user/colibry/opcuaRt/MIR1/my_private_key.pem"},
            {'robot_sender_defaultLatitude': 49.383224},
            {'robot_sender_defaultLongitude': 1.073758}
            ],
            name='robot_sender',
            output='screen',
            remappings=[
                #("robot_simulator_cmd_vel", "robot_sender_cmd_vel")
                #("/robot_sender_poseInUtmTiles", "/robot_simulator_poseInUtmTiles")
            ]
            )
    ld.add_action(node1)

 


    node2= launch_ros.actions.Node(
            package='colibry_robot_simulator',
            executable='robot_simulator',
            parameters=[
            {"robot_simulator_defaultLatitude": 49.383224},
            {'robot_simulator_defaultLongitude': 1.073758},
            {'robot_simulator_defaultYawDeg': 0.0}
            ],
            name='robot_simulator',
            output='screen',
            remappings=[
                #/turtle1/cmd_vel
                #("robot_simulator_poseInUtmTiles", "robot_sender_poseInUtmTiles")
                ("/robot_simulator_cmd_vel", "/robot_sender_cmd_vel"),
                #("/robot_simulator_cmd_vel", "/turtle1/cmd_vel"),#turle move
                ("/robot_simulator_poseInUtmTiles", "/robot_sender_poseInUtmTiles")
            ]
            )
    ld.add_action(node2)
    return ld

    """return launch.LaunchDescription([
        launch_ros.actions.Node(
            package='colibry_communicator',
            executable='robot_sender',
            name='robot_sender',
            output='screen',
            parameters=[
            {'toto': 10},
            {'robot_sender_FREQUENCY': 10},
            {'robot_sender_robotName': "Fab1(MIR)"},
            {'robot_sender_ENCRYPT': 0},
            {'robot_sender_url': "opc.tcp://127.0.0.1:4840/freeopcua/server/"},
            {'robot_sender_namespace': "http://esigelec.ddns.net"},
            {'robot_sender_certificate': "vincent/my_cert.der"},
            {'robot_sender_private_key': "vincent/my_private_key.pem"},
            {'robot_sender_defaultLatitude': 49.383224},
            {'robot_sender_defaultLongitude': 1.073758}
            ]
            ),

        launch_ros.actions.Node(
            package='colibry_robot_simulator',
            executable='robot_simulator',
            name='robot_simulator',
            output='screen'
            ),
    ])"""
#ros2 run colibry_robot_simulator robot_simulator
#ros2 run colibry_communicator robot_sender

