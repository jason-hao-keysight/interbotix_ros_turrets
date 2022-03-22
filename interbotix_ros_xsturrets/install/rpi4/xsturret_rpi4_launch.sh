#! /bin/bash

# This script is called by the xsturret_rpi4_Keysight_PathWave_Test_Automation_boot.service file when
# the Raspberry Pi boots. It sources the ROS related workspaces
# and launches the xsturret_control launch file.
# also launches RPiServoDriver.py python script for accepting commands
# from OpenTAP.Plugins.HornPositioner in Keysight PathWave Test Automation 

source /opt/ros/noetic/setup.bash
source /home/aaron/interbotix_ws/devel/setup.bash

launch_from_boot=false
if [ "$launch_from_boot" == true ] ; then
        echo "Launching..."
	roslaunch interbotix_xsturret_control xsturret_control.launch robot_model:=wxxms & python3 /home/aaron/interbotix_ws/src/interbotix_ros_turrets/interbotix_ros_xsturrets/install/rpi4/RPiServoDriver.py
else
        echo "Boot launch disabled"
fi
