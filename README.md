# inspector
Smart mapping based on ROS 

This system of stereographic inspection of the internal space of the pipeline allows you to build a three-dimensional map of the investigated object.  The usefulness of the project lies in the possibility of finding the pipeline by overlaying the scanned area on a two-dimensional map of the area.  It is proposed to use an accelerometer and magnetometer to determine the absolute course of the moving platform and determine the position of the robot based on the rotation of the actuators.

Three-dimensional survey will be carried out using SLAM algorithms.

It is possible to use the following mapping technologies:

https://github.com/OSLL/tiny-slam-ros
This package provides ROS implentation of the tinySLAM (https://openslam.org/tinyslam.html) that is one of the most simpliest and lightweight SLAM methods.

https://github.com/ros-perception/slam_gmapping
slam_gmapping contains a wrapper around gmapping which provides SLAM capabilities.
