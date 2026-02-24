import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # Define package and urdf file names
    pkg_name = 'amphi_description'
    urdf_file = 'amphi.urdf' # The name of your URDF file

    # Get the package share directory
    pkg_share = get_package_share_directory(pkg_name)

    # 1. Get the full path to the URDF file
    urdf_path = os.path.join(pkg_share, 'urdf', urdf_file)
    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()

    # 2. Set the GZ_SIM_RESOURCE_PATH
    # This is not strictly necessary for simple shapes but is good practice
    resource_env = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=os.path.join(pkg_share, '..')
    )

    # 3. Launch Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        # '-r' tells Gazebo to run the simulation right away
        launch_arguments={'gz_args': '-r empty.sdf'}.items(),
    )

    # 4. Spawn the robot entity in Gazebo
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', # This topic gets the URDF from robot_state_publisher
                   '-name', 'amphi_bot',          # The name of the robot in the simulation
                   '-z', '0.2'],                  # Spawn it 0.2m above the ground
        output='screen'
    )

    # 5. Publish robot state (TF transforms)
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_desc,
            'use_sim_time': True # MUST be true for simulation
        }]
    )

    # 6. Bridge to synchronize the clock
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
        output='screen'
    )

    # This is the list of all actions to be launched
    return LaunchDescription([
        resource_env,
        gazebo,
        robot_state_publisher,
        spawn_entity,
        bridge
    ])