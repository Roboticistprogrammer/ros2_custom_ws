"""Launch the YOLOv11 warehouse pallet detector node."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


PACKAGE_NAME = 'yolov11_warehouse_pallet_detector'


def generate_launch_description():
    """Generate the detector launch description."""
    default_model_path = PathJoinSubstitution([
        FindPackageShare(PACKAGE_NAME),
        'models',
        'whole_pallet_n_640.pt',
    ])

    model_path = LaunchConfiguration('model_path')
    image_topic = LaunchConfiguration('image_topic')
    annotated_image_topic = LaunchConfiguration('annotated_image_topic')
    detections_topic = LaunchConfiguration('detections_topic')
    confidence_threshold = LaunchConfiguration('confidence_threshold')
    device = LaunchConfiguration('device')
    use_sim_time = LaunchConfiguration('use_sim_time')

    detector_node = Node(
        package=PACKAGE_NAME,
        executable='yolov11_node',
        name='yolov11_detector',
        output='screen',
        parameters=[{
            'model_path': model_path,
            'image_topic': image_topic,
            'annotated_image_topic': annotated_image_topic,
            'detections_topic': detections_topic,
            'confidence_threshold': confidence_threshold,
            'device': device,
            'use_sim_time': use_sim_time,
        }],
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'model_path',
            default_value=default_model_path,
            description='Absolute path to the YOLOv11 .pt model file.',
        ),
        DeclareLaunchArgument(
            'image_topic',
            default_value='/camera/image_raw',
            description='Input camera image topic.',
        ),
        DeclareLaunchArgument(
            'annotated_image_topic',
            default_value='/camera/detections/image',
            description='Annotated output image topic.',
        ),
        DeclareLaunchArgument(
            'detections_topic',
            default_value='/camera/detections',
            description='Structured Detection2DArray output topic.',
        ),
        DeclareLaunchArgument(
            'confidence_threshold',
            default_value='0.25',
            description='Minimum YOLO confidence score for detections.',
        ),
        DeclareLaunchArgument(
            'device',
            default_value='',
            description='Ultralytics device override, for example cpu, 0, or cuda:0.',
        ),
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation time from Isaac Sim.',
        ),
        detector_node,
    ])
