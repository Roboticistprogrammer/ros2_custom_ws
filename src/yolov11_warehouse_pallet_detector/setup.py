from glob import glob
import os

from setuptools import find_packages, setup

package_name = 'yolov11_warehouse_pallet_detector'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'models'), glob('models/*')),
        (os.path.join('share', package_name, 'scripts'),
            glob('scripts/*.bash') + glob('scripts/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='amir',
    maintainer_email='amir.salar@example.com',
    description='ROS 2 YOLOv11 pallet detector for Isaac Sim warehouse camera streams.',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'yolov11_node = yolov11_warehouse_pallet_detector.yolov11_node:main',
        ],
    },
)
