cmake_minimum_required(VERSION 3.8)

cmake_minimum_required(VERSION 3.8)

project(humanoid_description)


find_package(ament_cmake REQUIRED)



# Install launch files

install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)



# Install robot description files

install(
  DIRECTORY urdf
  DESTINATION share/${PROJECT_NAME}
)



# Install controller configuration

install(
  DIRECTORY config
  DESTINATION share/${PROJECT_NAME}
)



ament_package()

