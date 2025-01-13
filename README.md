# F1Tenth_Braking_system
Emergency braking system algorithm for the RC car inside simulation environment

I implemented an Emergency Braking System feature by adding safety_node.py to the _open-source simulator F1Tenth Gym_. This stops the vehicle when too close to a wall (iTTC <1). The algorithm I used is
-  **iTTC = range / (-range)’**
> - Explanation: Time to collision = range / the rate of change in range (or velocity * cosθ).
> - Range and θ are acquired by using the library LaserScan messages and subscribing to /scan topic.
> - Velocity is calculated in 3D by using the library Odometry message and subscribing to /odom topic.
> - iTTC is then calculated using the above info and then gets published to /drive topic using AckermannDriveStamped. 
> - Configurations are then done in the .xml file and config.py to merge the node to the simulation.
> - Simulation is initiated with keyboard control activated. 
 
**To run this simulator**, assuming Docker Desktop is successfully installed and started up, do these following steps.

1.	If you are using Window, go to Command Prompt by typing cmd in your Window search bar.

2.	In the CMD, type this bash to install the simulator to your desired folder:
```
Git clone https://github.com/f1tenth/f1tenth_gym_ros
docker-compose up

```

3.	Open another terminal, run this bash to initiate the container:
```
docker exec -it f1tenth_gym_ros-sim-1 /bin/bash

```

4.	After the docker container is activated, run this bash to activate the simulator:
```
source /opt/ros/foxy/setup.bash
source install/setup.bash
ros2 launch f1tenth_gym_ros gym_bridge_launch.py

```
6.	Open a browser, the simulator will be running on **http://localhost:8080/vnc.html**. Click the _CONNECT_ button.

7.	Open another terminal, run this bash to initiate the container:
```
docker exec -it f1tenth_gym_ros-sim-1 /bin/bash

```

8.	After the docker container is activated, bash this to activate keyboard movement control:
```bash
source /opt/ros/foxy/setup.bash
source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard

```
> At this point, the car can move by using u  i  o
> 					   j  k  l
> 					   m  ,  .


Coding Features: Docker Compose runs the docker-compose.yml to launch the file onto noVNC on the local port. Preliminary objects setup are done in the config/sim.yaml file to set up the topics, set up the map based on a .png file and the location (x,y,z) of the car object on png. Then 2D is converted to 3D using transforms3d Python library in the gym_bridge.py .





