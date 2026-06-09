# YOLOv11 Warehouse Pallet Detector

ROS 2 Jazzy package for detecting warehouse pallets from an Isaac Sim camera
stream with a YOLOv11 model. The default model is packaged in `models/` and the
detector publishes both annotated images and structured 2D detections.

## Interfaces

Default input:

- `/camera/image_raw` (`sensor_msgs/msg/Image`)

Default outputs:

- `/camera/detections/image` (`sensor_msgs/msg/Image`)
- `/camera/detections` (`vision_msgs/msg/Detection2DArray`)

Launch parameters:

- `model_path`: YOLOv11 `.pt` model path
- `image_topic`: input camera image topic
- `annotated_image_topic`: annotated image output topic
- `detections_topic`: structured detections output topic
- `confidence_threshold`: minimum detection confidence
- `device`: Ultralytics device override such as `cpu`, `0`, or `cuda:0`
- `use_sim_time`: use Isaac Sim clock

## Setup

Install ROS dependencies:

```bash
sudo apt update
sudo apt install \
  ros-jazzy-cv-bridge \
  ros-jazzy-launch \
  ros-jazzy-launch-ros \
  ros-jazzy-rclpy \
  ros-jazzy-sensor-msgs \
  ros-jazzy-vision-msgs \
  python3-colcon-common-extensions
```

Create the isolated `uv` environment from this package directory:

```bash
source /opt/ros/jazzy/setup.bash
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
export PYTHONPATH="$(pwd)/.venv/lib/python3.12/site-packages:${PYTHONPATH}"
```

The `.venv` directory is local development state and should not be committed.

## Build

From the ROS workspace root:

```bash
source /opt/ros/jazzy/setup.bash
source src/yolov11_warehouse_pallet_detector/.venv/bin/activate
export PYTHONPATH="$(pwd)/src/yolov11_warehouse_pallet_detector/.venv/lib/python3.12/site-packages:${PYTHONPATH}"
colcon build --packages-select yolov11_warehouse_pallet_detector
source install/setup.bash
```

## Run

Launch with defaults:

```bash
ros2 launch yolov11_warehouse_pallet_detector yolov11_core.launch.py
```

Override model, topics, or threshold:

```bash
ros2 launch yolov11_warehouse_pallet_detector yolov11_core.launch.py \
  model_path:=/absolute/path/to/whole_pallet_n_640.pt \
  image_topic:=/camera/image_raw \
  annotated_image_topic:=/camera/detections/image \
  detections_topic:=/camera/detections \
  confidence_threshold:=0.35
```

Run the node directly:

```bash
ros2 run yolov11_warehouse_pallet_detector yolov11_node \
  --ros-args \
  -p image_topic:=/camera/image_raw \
  -p confidence_threshold:=0.25
```

## Isaac Sim

Source the helper when you only need the Isaac Sim paths:

```bash
source scripts/launch.bash
```

Start Isaac Sim and open a warehouse USD stage:

```bash
WAREHOUSE_USD=/absolute/path/to/warehouse_world.usd scripts/launch.bash start
```

The helper uses these defaults, which can be overridden before sourcing or
running the script:

```bash
export ISAACSIM_PATH=/mnt/e/isaacsim
export ISAACSIM=${ISAACSIM_PATH}/isaac-sim.bat
export ISAACSIM_PYTHON=${ISAACSIM_PATH}/python.bat
```

## Checks

```bash
python3 -m py_compile yolov11_warehouse_pallet_detector/yolov11_node.py
python3 -c "import rclpy, cv_bridge, vision_msgs, ultralytics; print('imports ok')"
colcon test --packages-select yolov11_warehouse_pallet_detector
colcon test-result --verbose
```
