from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

ARGUMENTS = [
    DeclareLaunchArgument(
        'config_name',
        default_value='Liguria',
        description='Nome del file YAML senza estensione'
    ),
    DeclareLaunchArgument(
        'namespace',
        default_value='/'
    ),
    DeclareLaunchArgument(
        'node_name',
        default_value='ntrip_client'
    ),
    DeclareLaunchArgument(
        'debug',
        default_value='false',
        choices=['true', 'false']
    ),
]


def launch_setup(context, *args, **kwargs):
  package_name = 'ntrip_client'
  package_share = get_package_share_directory(package_name)

  config_name = LaunchConfiguration('config_name').perform(context)
  namespace = LaunchConfiguration('namespace')
  node_name = LaunchConfiguration('node_name')
  debug = LaunchConfiguration('debug')

  config_file = os.path.join(
    package_share,
    'config',
    f'{config_name}.yaml'
  )
  
  if not os.path.exists(config_file):
    raise FileNotFoundError(f'Config file not found: {config_file}')

  ntrip_client_node = Node(
    package=package_name,
    executable='ntrip_ros.py',
    name=node_name,
    namespace=namespace,
    parameters=[config_file],
    output='screen',
    # remappings=[
    #     ('nmea', '/gx5/nmea/sentence')
    # ],
  )
  
  return [
    SetEnvironmentVariable(
        name='NTRIP_CLIENT_DEBUG',
        value=debug
    ),
    ntrip_client_node
  ]

def generate_launch_description():
  ld = LaunchDescription(ARGUMENTS)
  ld.add_action(OpaqueFunction(function=launch_setup))
  return ld