cmake_minimum_required(VERSION 3.8)

project(humanoid_description)


find_package(ament_cmake REQUIRED)


# =========================
# Install launch files
# =========================

install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)


# =========================
# Install robot description
# Keep urdf/modules structure
# =========================

install(
  DIRECTORY urdf
  DESTINATION share/${PROJECT_NAME}
)


# =========================
# Install config files
# =========================

install(
  DIRECTORY config
  DESTINATION share/${PROJECT_NAME}
)


# =========================
# Install Gazebo worlds
# =========================

install(
  DIRECTORY worlds
  DESTINATION share/${PROJECT_NAME}
)


ament_package()

