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
# Install URDF files
# =========================
# 只安装正式模型文件
# backup 文件不进入 install

install(
  DIRECTORY urdf
  DESTINATION share/${PROJECT_NAME}
  PATTERN "backup" EXCLUDE
  PATTERN "*.old" EXCLUDE
  PATTERN "*.bad" EXCLUDE
  PATTERN "*backup*" EXCLUDE
  PATTERN "*broken*" EXCLUDE
  PATTERN "*failed*" EXCLUDE
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
