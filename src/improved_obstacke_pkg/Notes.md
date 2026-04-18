Notes:

Separate Callbacks Architecture:

Your node should have two distinct callbacks:
scan_callback(): Receives and processes LiDAR data, updates internal state variables
timer_callback(): Reads the internal state and publishes velocity commands at a fixed rate
This separation provides better control over publishing frequency and prevents blocking
The timer should run at approximately 10 Hz (100ms interval) for smooth robot control

----

Single-Threaded Executor Implementation:

Use the default rclcpp::spin() which employs a single-threaded executor
All callbacks execute sequentially on one thread
No mutex required since there's no concurrent access to shared data
Simpler implementation, good for understanding basic ROS2 concepts
Callbacks will queue up if one takes too long

Multi-Threaded Executor Implementation:

Use rclcpp::executors::MultiThreadedExecutor with 2 or more threads
Callbacks can execute in parallel on different threads
Must use std::mutex and std::lock_guard to protect shared data (obstacle_ahead_, min_distance_)
Lock the mutex in both scan_callback() and timer_callback() when accessing shared variables
Better for systems with multiple sensors or computationally intensive operations

Thread Safety Best Practices:

Always use std::lock_guard<std::mutex> for automatic lock management
Keep critical sections (locked code) as short as possible
Never hold a lock while publishing or performing I/O operations if possible
Be aware of potential deadlocks when using multiple mutexes
RViz Configuration:

Create a config/ directory in your package
The RViz config file should:
Set the fixed frame to fastbot_1/base_laser_link
Add a LaserScan display subscribing to /fastbot_1/scan
Configure appropriate visualization settings (point size, color)
Set a suitable camera view (Orbit view works well)
Install the config directory in CMakeLists.txt using install(DIRECTORY config ...)

Obstacle Detection Logic:

Check the front 60-degree sector of the LiDAR scan (approximately indices from 5/12 to 7/12 of the array)
Find the minimum distance in this sector
Use a threshold of 0.6 meters to determine if an obstacle is present
Validate that measurements are within range_min and range_max before using them

Control Strategy:

When obstacle detected: linear.x = 0.0, angular.z = 0.5 (turn left)
When path is clear: linear.x = 0.2, angular.z = 0.0 (move forward)
Add informative log messages using RCLCPP_INFO() to track behavior
