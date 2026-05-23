import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from px4_msgs.msg import TrajectorySetpoint, VehicleCommand, OffboardControlMode, VehicleStatus

class ZenohAdvancedDemo(Node):
    def __init__(self):
        super().__init__('zenoh_advanced_demo')
        
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )
        
        # Publishers
        self.setpoint_pub = self.create_publisher(TrajectorySetpoint, '/fmu/in/trajectory_setpoint', qos_profile)
        self.offboard_mode_pub = self.create_publisher(OffboardControlMode, '/fmu/in/offboard_control_mode', qos_profile)
        self.cmd_pub = self.create_publisher(VehicleCommand, '/fmu/in/vehicle_command', qos_profile)
        
        # Subscriber (Listening to telemetry over Zenoh)
        self.status_sub = self.create_subscription(
            VehicleStatus, 
            '/fmu/out/vehicle_status', 
            self.status_callback, 
            qos_profile
        )
        
        self.timer = self.create_timer(0.1, self.timer_callback) 
        self.counter = 0
        self.current_nav_state = None

    def status_callback(self, msg):
        """Monitors flight controller telemetry streamed natively via Zenoh."""
        self.current_nav_state = msg.nav_state

    def send_command(self, command, param1=0.0, param2=0.0):
        msg = VehicleCommand()
        msg.command = command
        msg.param1 = param1
        msg.param2 = param2
        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        msg.from_external = True
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.cmd_pub.publish(msg)

    def timer_callback(self):
        # Stream baseline heartbeats
        offboard_msg = OffboardControlMode()
        offboard_msg.position = True
        offboard_msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.offboard_mode_pub.publish(offboard_msg)

        setpoint_msg = TrajectorySetpoint()
        setpoint_msg.position = [0.0, 0.0, -5.0] 
        setpoint_msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.setpoint_pub.publish(setpoint_msg)

        # Execute commands
        if self.counter == 20:
            self.get_logger().info("Requesting Offboard mode...")
            self.send_command(VehicleCommand.VEHICLE_CMD_DO_SET_MODE, 1.0, 6.0) 
        elif self.counter == 25:
            self.get_logger().info("Requesting Arm...")
            self.send_command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, 1.0)

        # Print current flight mode state caught from Zenoh every 2 seconds
        if self.counter % 20 == 0 and self.current_nav_state is not None:
            self.get_logger().info(f"Telemetry Update -> Current PX4 Nav State ID: {self.current_nav_state}")

        self.counter += 1

def main(args=None):
    rclpy.init(args=args)
    node = ZenohAdvancedDemo()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

