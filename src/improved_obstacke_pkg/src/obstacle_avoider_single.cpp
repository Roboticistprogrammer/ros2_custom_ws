#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include <cmath>

class ObstacleAvoiderSingle : public rclcpp::Node {
public:
  ObstacleAvoiderSingle()
      : Node("obstacle_avoider_single"), obstacle_ahead_(false) {
    // Subscriber for laser scan
    scan_sub_ = create_subscription<sensor_msgs::msg::LaserScan>(
        "fastbot_1/scan", 10,
        std::bind(&ObstacleAvoiderSingle::scan_callback, this,
                  std::placeholders::_1));

    // Publisher for velocity commands
    vel_pub_ =
        create_publisher<geometry_msgs::msg::Twist>("fastbot_1/cmd_vel", 10);

    // Timer for publishing velocity at 10 Hz
    timer_ = create_wall_timer(
        std::chrono::milliseconds(100),
        std::bind(&ObstacleAvoiderSingle::timer_callback, this));

    RCLCPP_INFO(get_logger(), "Single-threaded obstacle avoider started");
  }

private:
  void scan_callback(const sensor_msgs::msg::LaserScan::SharedPtr msg) {
    // Check front 60-degree sector (330° to 30°)
    size_t size = msg->ranges.size();
    size_t sector_size = size / 6;               // 60° worth of readings
    size_t right_start = size - sector_size / 2; // Start at 330°
    size_t left_end = sector_size / 2;           // End at 30°

    float min_dist = 6.0;

    // Check right side of front sector (330° to 360°)
    for (size_t i = right_start; i < size; i++) {
      if (std::isfinite(msg->ranges[i]) && msg->ranges[i] > msg->range_min &&
          msg->ranges[i] < msg->range_max) {
        min_dist = std::min(min_dist, msg->ranges[i]);
      }
    }

    // Check left side of front sector (0° to 30°)
    for (size_t i = 0; i < left_end; i++) {
      if (std::isfinite(msg->ranges[i]) && msg->ranges[i] > msg->range_min &&
          msg->ranges[i] < msg->range_max) {
        min_dist = std::min(min_dist, msg->ranges[i]);
      }
    }

    obstacle_ahead_ = (min_dist < 0.4);
    min_distance_ = min_dist;
  }

  void timer_callback() {
    auto msg = geometry_msgs::msg::Twist();

    if (obstacle_ahead_) {
      msg.linear.x = 0.0;
      msg.angular.z = 0.7; // Turn left
      RCLCPP_INFO(get_logger(), "Obstacle at %.2fm - Turning", min_distance_);
    } else {
      msg.linear.x = 0.2;
      msg.angular.z = 0.0;
      RCLCPP_INFO(get_logger(), "Clear path - Moving forward");
    }

    vel_pub_->publish(msg);
  }

  rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr scan_sub_;
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr vel_pub_;
  rclcpp::TimerBase::SharedPtr timer_;
  bool obstacle_ahead_;
  float min_distance_;
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<ObstacleAvoiderSingle>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
