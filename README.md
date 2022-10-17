# opcuaRt

projet to try to create an architecture to communicate with robots from/to Rtmaps and ROS

The basic example in rtmaps directory allowed the possibility to operate several robots (3) from a main controller with Xbox joysticK


# installs done :


under windows :
pip install asyncua

under  Ubuntu:
apt install python-opcua        # Library
apt install python-opcua-tools  # Command-line tools

work is based o git https://github.com/FreeOpcUa/opcua-asyncio

## starting 
* first create certificate with generate_certificate.sh

* To beguin to use it with your robots, modify file robotDescription.py file.
(The principe, is that all data availaibles in your robot will be availaible in the server area and client will have access to it)

* run the server (cd opcuaRt\server\ then python server-with-encryption.py)

* If you have rtmaps windows on your computer, you can open diagramme "rtmaps\robot1Diagram.rtd"

On the diagramme, 
* blue part it a rtmaps python component to control the robots (button LT is deadman, left joystick control longi and rot speed, button A is to control previous robot, button Y is to controll next robot )
* green part are component to read robot information (like wanted longi speed, rot speed), send to the server the current robot pose (mapId, lat, long, alt, roll, pitch, yaw(in rad)) and a simple pythonrobot simulator (simple runge Kutta simulation )
![](images/rtmapsdiagram.jpg )

When you run the diagram, you must obtain a qml windows with 3 robots simulated and the capacity to move the 3 robots with your xbox joystick

![](images/visualiser.jpg )

## know bug
* authentification with certificate is not working well with my anaconda from rtmaps under windows (but is working well from my anaconda), so encryption is disabled for the moment but can easily be enabled again

## comming soon 
    * ros node to interface a robot
    * next developements will be the availaibility to control other kind of robots

###########


