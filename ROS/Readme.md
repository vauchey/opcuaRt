#python ros components inspired from
https://www.theconstructsim.com/publish-position-robot-using-transformbroadcaster-python/

#git install
sudo apt install git-gui
git config --global user.nmame "myemal@toto.com"
#rajouter les lignes suviantes dans 
[user]
	name =user.name
	email = myemal@toto.com
	
	
#install ros2 and other
#sudo apt install catkin
#if needed :
#sudo apt install python3-catkin-pkg
#udo apt install python3-catkin
#sudo apt install python3-colcon-common-extensions
#ros2 run rviz2 rviz2
#catkin_DIR

#au final on va faire en ros 1 :
http://wiki.ros.org/noetic/Installation/Ubuntu

#cd /home/user/Colibry/opcuaRt/ROS/catkin_ws
cd /home/user/Colibry/opcuaRt/ROS/catkin_ws
catkin_make
source /home/user/Colibry/opcuaRt/ROS/catkin_ws/devel/setup.bash #you can addid in the ~.bashrc

---------------------------------
cd /home/user/Colibry/opcuaRt/ROS/catkin_ws/src
catkin_create_pkg colibry_communicator std_msgs rospy roscpp
cd /home/user/Colibry/opcuaRt/ROS/catkin_ws
catkin_make
source /home/user/Colibry/opcuaRt/ROS/catkin_ws/devel/setup.bash
roscd colibry_communicator
mkdir scripts
cd scripts
echo "#! /usr/bin/env python3"> communicator.py
chmod +x communicator.py
cd /home/user/Colibry/opcuaRt/ROS/catkin_ws
catkin_make

rosrun colibry_communicator communicator.py
sudo apt install python3-pip
pip install asyncua
pip install utm
pip install numpy
sudo apt install ipython3
pip install scipy
#sudo apt install ros-foxy-tf-transformations
#sudo pip3 install transforms3d
#lister des topic rostopic list
#visualiser un topich #rostopic echo /communicator_cmd_vel
rostopic echo turtle1/pose
#install anaconda and python https://phoenixnap.com/kb/how-to-install-anaconda-ubuntu-18-04-or-20-04
#sudo apt-get install curl
#curl –O https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
#bash ./Anaconda3-2022.10-Linux-x86_64.sh #install to /home/user/anaconda3

#open a new tab
#pip install asyncua
#pip install -U rospkg #apres avoir installe anaconda, il faut installer le rospkg
#sudo apt install python3-roslaunch# apres avoir installe annaconda, il faut le refaires

#simulatin d'un turlebot
#export TURTLEBOT3_MODEL=waffle
#sudo apt udpate
#sudo apt install ros-foxy-turtlebot3-description ros-foxy-turtlebot3-simulations ros-foxy-turtlebot3-bringup #ros-foxy-turtlebot3-navigation2 ros-foxy-turtlebot3 ros-foxy-xacro ros-foxy-turtlebot3-teleop #ros-foxy-turtlebot3-cartographer



#essai d'un simulator webots
sudo snap install webots
webots

#/snap/webots/22/usr/share/webots/
#cp -r <webots>/projects/languages/ros/webots_ros .
#cp -r <webots>/projects/default/controllers/ros/include/srv webots_ros/
#cp -r <webots>/projects/default/controllers/ros/include/msg webots_ros/
#install ros 2 with lxd
#https://ubuntu.com/blog/install-ros-2-humble-in-ubuntu-20-04-or-18-04-using-lxd-containers
#sudo snap install lxd
#sudo lxd init --minimal
#lxc launch images:ubuntu/22.04 ubuntu-container
#list all : lxc list
#get the shell:
#lxc exec ubuntu-container -- /bin/bash

#ros robot
https://www.theconstructsim.com/gazebo-5-minutes-003-spawn-robot-gazebo/


#
#mkdir -p gazeboSimulator/src
#cd gazeboSimulator/src
#git clone https://bitbucket.org/theconstructcore/two-wheeled-robot-simulation



#rosrun gazebo_ros gazebo
#rostopic echo /odom


cd gazeboSimulator
catkin_make
source devel/setup.bash
rospack profile
roslaunch m2wr_description spawn.launch