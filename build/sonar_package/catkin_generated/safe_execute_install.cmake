execute_process(COMMAND "/home/ubuntu/spring-2023-ros-workspace/build/sonar_package/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/ubuntu/spring-2023-ros-workspace/build/sonar_package/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
