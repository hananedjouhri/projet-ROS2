import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    # 1. Définition des chemins
    pkg_path = get_package_share_directory('mobile_robot')
    
    # 2. Traitement du fichier robot (XACRO)
    xacro_file = os.path.join(pkg_path, 'model', 'robot.xacro')
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    # 3. Noeud Robot State Publisher
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw, 'use_sim_time': True}]
    )

    # 4. Lancement de Gazebo (monde vide)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
        launch_arguments={'gz_args': '-r empty.sdf'}.items(),
    )

    # 5. Apparition du robot dans Gazebo
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-name', 'mon_robot'],
        output='screen'
    )

    # 6. Le Pont (Bridge) pour le laser et les commandes
    # On utilise le dossier "params" (vérifie qu'il s'appelle bien comme ça !)
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={os.path.join(pkg_path, "params", "bridge_parameters.yaml")}',
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        node_robot_state_publisher,
        spawn_entity,
        bridge
    ])