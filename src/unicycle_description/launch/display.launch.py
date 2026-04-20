import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    package_name = 'unicycle_description'
    pkg_share = get_package_share_directory(package_name)

    tb3_share = get_package_share_directory('turtlebot3_description')
    xacro_file = os.path.join(tb3_share, 'urdf', 'turtlebot3_burger.urdf')

    robot_description_config = xacro.process_file(xacro_file, mappings={'robot_namespace': ''})
    robot_desc = robot_description_config.toxml()
    
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{'robot_description': robot_desc}]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', os.path.join(pkg_share, 'rviz', 'simulation.rviz')]
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher'
    )

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_node,
        rviz_node,
        # Dodajemy statyczne połączenie odom -> base_link, żeby RViz wiedział gdzie jest robot
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0', '0', '0', '0', '0', '0', 'odom', 'base_footprint']
        )
    ])