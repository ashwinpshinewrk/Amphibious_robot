cmake_minimum_required(VERSION 3.8)
project(amphi_control)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(hardware_interface REQUIRED)
find_package(pluginlib REQUIRED)
find_package(PkgConfig REQUIRED)
pkg_check_modules(Serial REQUIRED IMPORTED_TARGET libserial)

add_library(${PROJECT_NAME} SHARED src/amphi_system.cpp)

ament_target_dependencies(${PROJECT_NAME}
  "rclcpp"
  "hardware_interface"
  "pluginlib"
)

target_include_directories(${PROJECT_NAME} PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include> $<INSTALL_INTERFACE:include>)

target_link_libraries(${PROJECT_NAME}
  PkgConfig::Serial # AI told me this is external file?? 
)

# used for pluginlib , to make it dynamic , FOR MANUAL AND AUTO i suppose. Makes it a plugin for ros2_control
#pluginlib_export_plugin_description_file(hardware_interface amphi_control.xml)

install(TARGETS
  ${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

install(DIRECTORY
  include/
  DESTINATION include)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
