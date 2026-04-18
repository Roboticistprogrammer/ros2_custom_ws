from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_dir = get_package_share_directory('improved_obstacle_pkg')
    rviz_config = os.path.join(pkg_dir, 'config', 'obstacle_avoidance.rviz')
    
    return LaunchDescription([
        Node(
            package='improved_obstacle_pkg',
            executable='avoider_multi',
            output='screen'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config],
            output='screen'
        )
    ])
