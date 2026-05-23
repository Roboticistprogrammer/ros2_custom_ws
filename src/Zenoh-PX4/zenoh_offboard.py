import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from px4_msgs.msg import TrajectorySetpoint, VehicleCommand, OffboardControlMode

class ZenohSimulationTest(Node):
    def __init__(self):
        super().__init__('zenoh_simulation_test')
        
        # Best Effort QoS is required for high-rate PX4 setpoints over Zenoh
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
        
        # Loop variables (10Hz loop)
        self.timer = self.create_timer(0.1, self.timer_callback) 
        self.counter = 0

    def send_command(self, command, param1=0.0, param2=0.0):
        """Helper to safely format and send a vehicle command string."""
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
        # --- CRITICAL: Always stream the Offboard Control Mode Heartbeat ---
        offboard_msg = OffboardControlMode()
        offboard_msg.position = True   # We are telling PX4 we will provide position setpoints
        offboard_msg.velocity = False
        offboard_msg.acceleration = False
        offboard_msg.attitude = False
        offboard_msg.body_rate = False
        offboard_msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.offboard_mode_pub.publish(offboard_msg)

        # --- Stream the actual Target Position ---
        setpoint_msg = TrajectorySetpoint()
        setpoint_msg.position = [0.0, 0.0, -5.0] # NED coordinates: Go up 5 meters
        setpoint_msg.yaw = 0.0
        setpoint_msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.setpoint_pub.publish(setpoint_msg)

        # --- Delayed State Changes ---
        # Allow 2 seconds (20 ticks at 10Hz) of continuous streaming so PX4 accepts the mode
        if self.counter == 20:
            self.get_logger().info("PX4 has baseline signals. Switching to Offboard mode...")
            self.send_command(VehicleCommand.VEHICLE_CMD_DO_SET_MODE, 1.0, 6.0) # 1=Custom, 6=Offboard
            
        elif self.counter == 25:
            self.get_logger().info("Arming drone...")
            self.send_command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, 1.0) # 1.0 = Arm

        self.counter += 1

def main(args=None):
    rclpy.init(args=args)
    node = ZenohSimulationTest()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

