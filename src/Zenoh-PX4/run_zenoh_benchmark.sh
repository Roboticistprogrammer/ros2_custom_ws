#!/bin/bash
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
export ROS_DOMAIN_ID=0

# 1. Start the Zenoh Daemon Router in the background
ros2 run rmw_zenoh_cpp rmw_zenohd &
ZENOHD_PID=$!

# 2. Start the Native Zenoh PX4 SITL target
cd ~/PX4-Autopilot
make px4_sitl_zenoh &
PX4_PID=$!

sleep 5 # Wait for initialization

# 3. Start the Resource Monitor tracking the Zenoh daemon router
python3 ~/monitor_resources.py rmw_zenohd &
MONITOR_PID=$!

# 4. Run your Zenoh ROS 2 Offboard flight script
python3 ~/zenoh_offboard_test.py

# Cleanup after flight test completes
kill $ZENOHD_PID $PX4_PID $MONITOR_PID

