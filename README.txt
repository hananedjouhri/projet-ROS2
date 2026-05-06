===========================================================
GUIDE DE LANCEMENT : PROJET ROBOT AUTONOME (ROS 2 JAZZY)
===========================================================

Suivez l'ordre des terminaux pour un fonctionnement correct.

-----------------------------------------------------------
1️⃣ TERMINAL 1 : Simulation Gazebo
-----------------------------------------------------------
cd ~/ws_mobile_robot
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch mobile_robot gazebo_model.launch.py

-----------------------------------------------------------
2️⃣ TERMINAL 2 : Bridge (Laser + Moteurs + Caméra)
-----------------------------------------------------------
source /opt/ros/jazzy/setup.bash
ros2 run ros_gz_bridge parameter_bridge /scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan /cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist /camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image

-----------------------------------------------------------
3️⃣ TERMINAL 3 : RViz2 (Visualisation)
-----------------------------------------------------------
source /opt/ros/jazzy/setup.bash
rviz2

👉 NOTE : Si RViz est vide, faites : File > Open Config 
Puis sélectionnez : ~/ws_mobile_robot/src/mobile_robot/final_robot_config.rviz

-----------------------------------------------------------
4️⃣ TERMINAL 4 : Algorithme d'Autonomie (Python)
-----------------------------------------------------------
python3 ~/ws_mobile_robot/src/mobile_robot/model/obstacle_avoidance.py

-----------------------------------------------------------
🛑 COMMANDE POUR STOPPER LE ROBOT
-----------------------------------------------------------
source /opt/ros/jazzy/setup.bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{}"
===========================================================
