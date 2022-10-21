#! /usr/bin/env python3

from tf import TransformBroadcaster
import rospy
from rospy import Time 
from geometry_msgs.msg import Twist


import asyncio
import logging
import sys
import os
import time
import asyncua




DEBUG=True
#rostopic echo rosout

def myPrint(msg):
    if DEBUG:
        #rospy.loginfo(msg)
        print(msg)


sys.path.append( os.path.abspath(sys.path[0]+"/../../../../../"))

#import to know the robots
from robotDescription import *
#import to do client gesture
from ClientGesture import *


def getCurrentFileName():
    """function to get current filename without slash or extension"""
    return __file__.split("/")[-1].split(".")[0]

def getParameter(parameterName):
    """simple function to get easily paramter"""
    fullParameterName=getCurrentFileName()+"_"+str(parameterName)
    if rospy.has_param('/'+fullParameterName):
        return rospy.get_param('/'+fullParameterName)
    else:
        raise ValueError("parameter "+str(fullParameterName)+"is missing!!")

def main():
    rospy.init_node('my_broadcaster')
    
    myPrint("!!!!!!!!!!!!!!!!!!sys.path="+str(sys.path))

    #get parameters
    robotName=getParameter("robotName")
    url=getParameter("url")
    namespace=getParameter("namespace")
    certificate=getParameter("certificate")
    private_key=getParameter("private_key")
    ENCRYPT=getParameter("ENCRYPT")


    
    myPrint ("robotName="+str(robotName))
    myPrint ("url="+str(url))
    myPrint ("namespace="+str(namespace))
    myPrint ("certificate="+str(certificate))
    myPrint ("private_key="+str(private_key))
    myPrint ("ENCRYPT="+str(ENCRYPT))
 
    listOfName = listNames()
    myPrint ("robotName availaibles="+str(listOfName))

    currentRobotDescription = getCurrentRobotName(robotName)


    clientGesture = ClientGesture(url,namespace,certificate,private_key,ENCRYPT,currentRobotDescription)
    asyncio.run(clientGesture.connect())#do a connection

    #initiallisation des topics 
    pubVelocity = rospy.Publisher('cmd_vel', Twist, queue_size=10)


    #
    b = TransformBroadcaster()
    
    translation = (0.0, 0.0, 0.0)
    rotation = (0.0, 0.0, 0.0, 1.0)
    rate = rospy.Rate(5)  # 5hz
    
    x, y = 0.0, 0.0
    
    while not rospy.is_shutdown():
        if x >= 2:
            x, y = 0.0, 0.0 
        
        x += 0.1
        y += 0.1
        #rospy.loginfo("!!x")
        translation = (x, y, 0.0)
        #myPrint("x")
        
        b.sendTransform(translation, rotation, Time.now(), 'ignite_robot', '/world')

        #send a new position only if neede
        #asyncio.run(self.clientGesture.setPosition(timeStamp,-1,data))#run a processing

        asyncio.run(clientGesture.readRobot())
        myPrint ("robotGet.ts_map_id_posexyzrxryrz="+str(clientGesture.currentRobotDescription.ts_map_id_posexyzrxryrz))
		

        #sortie de la commande venant du server
        wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec=clientGesture.currentRobotDescription.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec
        myPrint ("wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec="+str(wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec))
		
        twist = Twist()
        if wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec[1] :
            twist.linear.x = wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec[2] #already meter by sec
            twist.linear.y = 1.0
            twist.linear.z = 0.0

            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec[3]#rad by sec
        else:
            twist.linear.x  =0.0
            twist.linear.y  =1.0
            twist.linear.z  =0.0
            twist.angular.x =0.0
            twist.angular.y =0.0
            twist.angular.z =0.0

        pubVelocity.publish(twist)


        rate.sleep()
    


if __name__ == '__main__':
    main()
