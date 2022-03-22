touch xsturret_rpi4_OpenTAP_boot.service
INTERBOTIX_WS=~/interbotix_ws
echo -e "
# This service auto-launches the xsturret_joy.launch file when the computer boots.
# This file should be copied to /lib/systemd/system. Afterwards, type...
# 'sudo systemctl daemon-reload' followed by 'sudo systemctl enable xsturret_rpi4_boot.service'.

[Unit]
Description=Start X-Series Turret Keysight PathWave Test Automation Control

[Service]
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/"$USER".Xauthority
ExecStart=/home/"$USER"/interbotix_ws/src/interbotix_ros_turrets/interbotix_ros_xsturrets/install/rpi4/xsturret_rpi4_launch.sh
Restart=on-failure

[Install]
WantedBy=graphical.target

" > xsturret_rpi4_OpenTAP_boot.service

chmod +x xsturret_rpi4_launch.sh
sudo cp xsturret_rpi4_boot.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable xsturret_rpi4_boot.service
echo -e "hdmi_force_hotplug=1\nhdmi_group=2\nhdmi_mode=82" | sudo tee -a /boot/firmware/usercfg.txt > /dev/null
