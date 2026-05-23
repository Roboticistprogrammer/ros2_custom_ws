#!/bin/bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp # Or rmw_fastrtps_cpp

# 1. Start the Micro-XRCE-DDS Agent in the background
MicroXRCEAgent udp4 -p 8888 &
AGENT_PID=$!

# 2. Start your standard PX4 SITL target (which connects to the XRCE Agent)
cd ~/PX4-Autopilot
make px4_sitl default &
PX4_PID=$!

sleep 5 # Wait for initialization

# 3. Start the Resource Monitor tracking the XRCE Agent middleman
python3 ~/monitor_resources.py MicroXRCEAgent &
MONITOR_PID=$!

# 4. Run your ROS 2 Offboard flight script (modified for standard DDS)
python3 ~/dds_offboard_test.py

# Cleanup after flight test completes
kill $AGENT_PID $PX4_PID $MONITOR_PID

