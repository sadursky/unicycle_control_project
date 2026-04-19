import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('unicycle_brain')
   
    trajectory_gen_node = Node(
        package='unicycle_brain',
        executable='trajectory_generator',
        name='trajectory_generator'
    )

    config_path = os.path.join(pkg_share, 'config', 'pid_params.yaml')
    controller_node = Node(
        package='unicycle_brain',
        executable='controller',
        name='controller',
        parameters=[config_path]
    )

    robot_model_node = Node(
        package='unicycle_brain',
        executable='robot_model',
        name='robot_model'
    )

    return LaunchDescription([
        trajectory_gen_node,
        controller_node,
        robot_model_node
    ])
