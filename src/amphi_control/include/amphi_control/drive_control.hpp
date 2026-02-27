#ifndef AMPHI_SYSTEM_HPP
#define AMPHI_SYSTEM_HPP

#include "hardware_interface/system_interface.hpp"
#include "rclcpp/rclcpp.hpp"
#include <libserial/SerialPort.h>
#include <vector>

namespace amphi_control {

class AmphiSystem : public hardware_interface::SystemInterface {
public:
  //  During initialization and the info variable if data from configs like URDF
  hardware_interface::CallbackReturn
  on_init(const hardware_interface::HardwareInfo &info) override;

  // An array of Interfaces for to show which feedback values can be availed
  std::vector<hardware_interface::StateInterface>
  export_state_interfaces() override;
  // Implement set point for hardware , like target velocity
  std::vector<hardware_interface::CommandInterface>
  export_command_interfaces() override;
  // For hardware communication
  hardware_interface::CallbackReturn
  on_configure(const rclcpp_lifecycle::State &previous_state) override;
  // closing the communication
  hardware_interface::CallbackReturn
  on_cleanup(const rclcpp_lifecycle::State &previous_state) override;

  hardware_interface::return_type read(const rclcpp::Time &time,
                                       const rclcpp::Duration &period) override;
  hardware_interface::return_type
  write(const rclcpp::Time &time, const rclcpp::Duration &period) override;

private:
  // To store command of PI
  double cmd_left_screw;
  double cmd_right_screw;

  // store current state of motors to give to esp32
  double vel_left_screw;
  double vel_right_screw;
  // connection object
  LibSerial::SerialPort serial_port;
};
} // namespace amphi_control

#endif // AMPHI_SYSTEM_HPP
