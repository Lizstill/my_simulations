# my_simulations
This is the turtlebot3 simulations and maze solving algorithms for Noetic and python3
The unknown_maze.py algorithum uses cycles through find wall, follow wall and turn left as a streamline method of implementing the right hand rule for any maze in gazebo.
The known_right_maze.py has direction ranges where if the robot is a certain distance from each wall, the turtlebot will either continue straight with three different speeds, reverse, turn counterclockwise or clockwise.
If the mazes are smaller than the ones that I used. I would slow down the linear velocity and the angular velocity of the robot. If th emaze includes a series of tight turns,
I would also try to include a dely before the turn left and the follow the wall functions so that the robot is able to clear and wall's corner.
The lidar scans are set for gazebo with the 360 degrees scanner.
Os: Ubuntu 20.04
ROS: ROS Noetic
Packages Used: Turtlebot3
https://github.com/ROBOTIS-GIT/turtlebot3/tree/noetic-devel
git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
git clone https://github.com/ROBOTIS-GIT/turtlebot3.git
git clone https://github.com/ROBOTIS-GITT
THe turtlebot comes in 3 different models: Burger, waffel and waffel_pie. I used burger for each of the mazes. 
$ export TURTLEBOT3_MODEL=burger
This is to check on the ranges of the lidar and make the python files executable. Make sure to do this with the other python codes and to add each file to your workspace. 
$ gedit laser_data.py
$ gedit avoid_obstacle.py
$ chmod +x avoid_obstacle.py
I do not take credit for the turtlebot files. I have only contributed to changing the unknown_maze.py and known_right_maze.py files. 
