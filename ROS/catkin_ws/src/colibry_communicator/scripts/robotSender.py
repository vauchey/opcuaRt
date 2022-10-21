#! /usr/bin/env python3

from tf import TransformBroadcaster
import rospy
from rospy import Time 
from geometry_msgs.msg import Twist
from sensor_msgs.msg import NavSatFix

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



class Comunicator:
    def __init__(self):
        

        myPrint("!!!!!!!!!!!!!!!!!!sys.path="+str(sys.path))

        #get parameters
        self.robotName=getParameter("robotName")
        self.url=getParameter("url")
        self.namespace=getParameter("namespace")
        self.certificate=getParameter("certificate")
        self.private_key=getParameter("private_key")
        self.ENCRYPT=getParameter("ENCRYPT")


        
        myPrint ("robotName="+str(self.robotName))
        myPrint ("url="+str(self.url))
        myPrint ("namespace="+str(self.namespace))
        myPrint ("certificate="+str(self.certificate))
        myPrint ("private_key="+str(self.private_key))
        myPrint ("ENCRYPT="+str(self.ENCRYPT))
    
        listOfName = listNames()
        myPrint ("robotName availaibles="+str(listOfName))

        currentRobotDescription = getCurrentRobotName(self.robotName)


        self.clientGesture = ClientGesture(self.url,self.namespace,self.certificate,self.private_key,self.ENCRYPT,currentRobotDescription)
        asyncio.run(self.clientGesture.connect())#do a connection

        #initiallisation des topics 
        self.pubVelocity = rospy.Publisher(getCurrentFileName()+"_"+'cmd_vel', Twist, queue_size=10)

        pass
    def process(self):
        #send a new position only if neede
        #asyncio.run(self.clientGesture.setPosition(timeStamp,-1,data))#run a processing

        asyncio.run(self.clientGesture.readRobot())
        myPrint ("robotGet.ts_map_id_posexyzrxryrz="+str(self.clientGesture.currentRobotDescription.ts_map_id_posexyzrxryrz))
		

        #sortie de la commande venant du server
        wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec=self.clientGesture.currentRobotDescription.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec
        myPrint ("wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec="+str(wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec))
		
        twist = Twist()
        if wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec[1] :
            twist.linear.x = wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec[2] #already meter by sec
            twist.linear.y = 0.0
            twist.linear.z = 0.0

            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec[3]#rad by sec
        else:
            twist.linear.x  =0.0
            twist.linear.y  =0.0
            twist.linear.z  =0.0
            twist.angular.x =0.0
            twist.angular.y =0.0
            twist.angular.z =0.0

        self.pubVelocity.publish(twist)

    def callBackNavSatFix(NavSatFix):
        print ("ttttttcallBackNavSatFix(navSatFix)")

    def callBackTwist(Twist):
        print ("yyyyyyycallBackTwist(Twist)")


def main():
    rospy.init_node('my_broadcaster')
    
   
    communicator = Comunicator()

    communicator_FREQUENCY=getParameter("FREQUENCY")
    


    """rospy.Subscriber(getCurrentFileName()+"_"+"navSatFix", NavSatFix, communicator.callBackNavSatFix)
    rospy.Subscriber(getCurrentFileName()+"_"+"poseInUtmTiles", Twist, communicator.callBackTwist)
    rospy.spin()
    """

    
    rate = rospy.Rate(communicator_FREQUENCY)  # 5hz
    
  
    
    while not rospy.is_shutdown():
        
        communicator.process()
        #faire un multiple subscriber, + un wakeup
        


        rate.sleep()
    


if __name__ == '__main__':
    main()
