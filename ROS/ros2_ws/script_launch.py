import launch
import launch_ros.actions

def generate_launch_description():
    return launch.LaunchDescription([
        launch_ros.actions.Node(
            package='colibry_communicator',
            executable='robot_sender',
            name='robot_sender'),
  ])
