#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include <cmath>
#include <mutex>

class ObstacleAvoiderMulti : public rclcpp::Node {
public:
  ObstacleAvoiderMulti()
      : Node("obstacle_avoider_multi"), obstacle_ahead_(false) {
    scan_sub_ = create_subscription<sensor_msgs::msg::LaserScan>(
        "fastbot_1/scan", 10,
        std::bind(&ObstacleAvoiderMulti::scan_callback, this,
                  std::placeholders::_1));

    vel_pub_ =
        create_publisher<geometry_msgs::msg::Twist>("fastbot_1/cmd_vel", 10);

    timer_ = create_wall_timer(
        std::chrono::milliseconds(100),
        std::bind(&ObstacleAvoiderMulti::timer_callback, this));

    RCLCPP_INFO(get_logger(), "Multi-threaded obstacle avoider started");
  }

private:
  void scan_callback(const sensor_msgs::msg::LaserScan::SharedPtr msg) {
    std::lock_guard<std::mutex> lock(data_mutex_);

    size_t size = msg->ranges.size();
    size_t sector_size = size / 6;               // 60° worth of readings
    size_t right_start = size - sector_size / 2; // Start at 330°
    size_t left_end = sector_size / 2;           // End at 30°

    float min_dist = 10.0;

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

    obstacle_ahead_ = (min_dist < 0.6);
    min_distance_ = min_dist;
  }

  void timer_callback() {
    std::lock_guard<std::mutex> lock(data_mutex_);

    auto msg = geometry_msgs::msg::Twist();

    if (obstacle_ahead_) {
      msg.linear.x = 0.0;
      msg.angular.z = 0.5;
      RCLCPP_INFO(get_logger(), "[MULTI] Obstacle at %.2fm - Turning",
                  min_distance_);
    } else {
      msg.linear.x = 0.2;
      msg.angular.z = 0.0;
      RCLCPP_INFO(get_logger(), "[MULTI] Clear path - Moving forward");
    }

    vel_pub_->publish(msg);
  }

  rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr scan_sub_;
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr vel_pub_;
  rclcpp::TimerBase::SharedPtr timer_;
  std::mutex data_mutex_;
  bool obstacle_ahead_;
  float min_distance_;
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<ObstacleAvoiderMulti>();

  // Use multi-threaded executor with 2 threads
  rclcpp::executors::MultiThreadedExecutor executor(rclcpp::ExecutorOptions(),
                                                    2);
  executor.add_node(node);
  executor.spin();

  rclcpp::shutdown();
  return 0;
}
