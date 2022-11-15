#! /usr/bin/env python3




import rclpy
from rclpy.clock import Clock
from rcl_interfaces.msg import ParameterDescriptor

from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from sensor_msgs.msg import NavSatFix


#pip install scipy
from scipy.spatial.transform import Rotation as R
import math

import threading

import asyncio
import logging
import sys
import os
import time
import asyncua

#pip install utm
import utm





DEBUG=True
#rostopic echo rosout


if DEBUG :
    logging.basicConfig(level=logging.INFO)
    _logger = logging.getLogger("asyncua")
else:
    logging.basicConfig(level=logging.ERROR)

#logging.basicConfig(level=logging.ERROR)


def myPrint(msg):
    if DEBUG:
        #rclpy.loginfo(msg)
        print(msg)

#print ("sys.path[0]="+str(sys.path[0]))
#sys.path.append( os.path.abspath(sys.path[0]+"/../../../../../"))
sys.path.append( os.path.abspath(sys.path[0]+"/../../../../../../"))#for ros2 arch

#import to know the robots
from robotDescription import *
#import to do client gesture
from ClientGesture import *


def getCurrentFileName():
    """function to get current filename without slash or extension"""
    return __file__.split("/")[-1].split(".")[0]

def getParameter(node,parameterName):
    """simple function to get easily paramter"""
    fullParameterName=getCurrentFileName()+"_"+str(parameterName)
  
    #node.declare_parameter(fullParameterName,None,dynamic_typing=True)
    #node.declare_parameter(fullParameterName,dynamic_typing=True)
    #node.declare_parameter(fullParameterName,"")
    parameter=ParameterDescriptor()
    parameter.dynamic_typing=True
    node.declare_parameter(fullParameterName,descriptor=parameter)
    parameterValue = node.get_parameter_or(fullParameterName)
    if parameterValue.value is None :
        raise ValueError("parameter "+str(fullParameterName)+" is missing!!")
    #assert( (parameterValue.value is not None), "parameter "+str(fullParameterName)+" is missing!!" )
    return parameterValue.value
   

class ClientGestureROS(ClientGesture):
    def __init__(self,url,namespace, certificate, private_key,ENCRYPT,currentRobotDescription):
        super().__init__(url,namespace, certificate, private_key,ENCRYPT,currentRobotDescription)



    def isDying(self):
        """function to redefine for ros or rtmaps, for example on rtmaps it will be rt.is_dying()"""
        if self.rclpy.ok():
            return False
        else:
            return True


    def sendRobotInformations(self,robotGet):
        """function to redefine for ros or rtmaps, for example on rtmaps it will be start writing, and on ros a publisher"""
        print ("sendRobotInformations from ROS2 :: wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec ="+str(robotGet.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec))
        print ("sendRobotInformations from ROS2 :: ts_map_id_posexyzrxryrz ="+str(robotGet.ts_map_id_posexyzrxryrz))
        print ("sendRobotInformations  from ROS2:: wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec ="+str(robotGet.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec))
		
        wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec= robotGet.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec
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

class RobotSender:
    def __init__(self,rclpy,node):
        

        #myPrint("!!!!!!!!!!!!!!!!!!sys.path="+str(sys.path))
       
        #get parameters
        self.node = node
        self.rclpy= rclpy
        self.robotName=getParameter(self.node,"robotName")
        self.url=getParameter(self.node,"url")
        self.namespace=getParameter(self.node,"namespace")
        self.certificate=getParameter(self.node,"certificate")
        self.private_key=getParameter(self.node,"private_key")
        self.ENCRYPT=getParameter(self.node,"ENCRYPT")
        self.robot_sender_FREQUENCY=getParameter(self.node,"FREQUENCY")
        self.robot_sender_Period=1/self.robot_sender_FREQUENCY
        #init parameters
        self.utmx=None
        self.utmy=None
        self.altitude=None
        self.zoneNumber=None
        self.zoneLetter=None
        self.roll=None
        self.pitch=None
        self.yaw=None

        self.newData=False

        #try to get some default zone number and letter by using defaultLaitude and Longitude
        try :
            self.latitude=getParameter(self.node,"defaultLatitude")
        except :
            self.latitude=None

        try :
            self.lontitude=getParameter(self.node,"defaultLongitude")
        except :
            self.lontitude=None
        #try to get zone number and letter
        try:
            utmX, utmY, zoneNumber, zoneLetter = utm.from_latlon( self.latitude, self.lontitude)
            self.zoneNumber=zoneNumber
            self.zoneLetter=zoneLetter
        except:
            pass

        

        myPrint ("robotName="+str(self.robotName))
        myPrint ("url="+str(self.url))
        myPrint ("namespace="+str(self.namespace))
        myPrint ("certificate="+str(self.certificate))
        myPrint ("private_key="+str(self.private_key))
        myPrint ("ENCRYPT="+str(self.ENCRYPT))

    
        listOfName = listNames()
        myPrint ("robotName availaibles="+str(listOfName))

        currentRobotDescription = getCurrentRobotName(self.robotName)


        
        self.clientGesture = ClientGestureROS(self.url,self.namespace,self.certificate,self.private_key,self.ENCRYPT,currentRobotDescription)
        #rajout des object necessaires a rose
        self.clientGesture.node=node
        self.clientGesture.rclpy=rclpy

        #initiallisation des topics out
        #self.pubVelocity = rclpy.Publisher(getCurrentFileName()+"_"+'cmd_vel', Twist, queue_size=10)
        #self.pubVelocity = rclpy.Publisher(getCurrentFileName()+"_"+'cmd_vel', Twist, queue_size=10)
        self.pubVelocity = self.node.create_publisher(Twist, getCurrentFileName()+"_"+'cmd_vel'  , 10)
        self.clientGesture.pubVelocity=self.pubVelocity


        #run the thread and wait it
        self.clientGesture.creaThreadAndRunIt(self.robot_sender_Period)
        while self.clientGesture.getIsReady() == False:
            time.sleep(0.5)         
        #asyncio.run(self.clientGesture.connect())#do a connection

        
        

        pass



    def callBackNavSatFix(self,navSatFix):

          #try to get zone number and letter
        try:
            utmX, utmY, zoneNumber, zoneLetter = utm.from_latlon( navSatFix.latitude, navSatFix.longitude )
            self.zoneNumber=zoneNumber
            self.zoneLetter=zoneLetter
        except:
            pass

        self.utmx= utmX
        self.utmy= utmY
        self.altitude= navSatFix.altitude
        
        self.sendPose()

        pass



    def callBackTwist(self,twist):

        self.utmx= twist.linear.x
        self.utmy= twist.linear.y
        self.altitude= twist.linear.z
        self.roll= twist.angular.x
        self.pitch= twist.angular.y
        self.yaw= twist.angular.z

        self.sendPose()

        pass



    def callBackImu(self,imu):
        quat=[imu.orientation.w,imu.orientation.x,imu.orientation.y,imu.orientation.z]
        [roll, pitch, yaw]= R.from_quat(quat).as_euler("ZYX",degrees=False)
        self.roll=roll
        self.pitch=pitch
        self.yaw=(math.pi/2.0)-yaw

        self.sendPose()


    def sendPose(self):
        """send current robot pose to server"""

        if ( \
            (self.utmx is not None) \
            and \
            (self.utmy is not None)  
            and \
            (self.altitude is not None)  \
            and \
            (self.zoneNumber is not None)  \
            and \
            (self.zoneLetter is not None)  \
            and \
            (self.roll is not None)  \
             and \
            (self.pitch is not None)  \
             and \
            (self.yaw is not None)  \
            ):

            #myPrint ("send to server !!!!!!!!!!")
            lati,longi = utm.to_latlon(self.utmx,self.utmy,self.zoneNumber,self.zoneLetter)

            self.timeStamp=(Clock().now().nanoseconds/1000)#time us us
            self.data=[lati,longi, self.altitude,self.roll, self.pitch, self.yaw]#must be a list
            myPrint ("send to server !!!!!!!!!!"+str(self.data))
            self.clientGesture.setPosition(self.timeStamp,-1,self.data)

            #self.newData=True
            #asyncio.run(self.clientGesture.setPosition(timeStamp,-1,data))#run a processing

            #asyncio.run(self.clientGesture.readRobot())
            #print ("robotGet.ts_map_id_posexyzrxryrz="+str(self.clientGesture.currentRobotDescription.ts_map_id_posexyzrxryrz))
def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node("robot_sender")
    robotSender = RobotSender(rclpy,node)


    node.create_subscription(NavSatFix, getCurrentFileName()+"_"+"navSatFix",robotSender.callBackNavSatFix,10)
    node.create_subscription(Imu, getCurrentFileName()+"_"+"imu",robotSender.callBackImu,10)
    node.create_subscription(Twist, getCurrentFileName()+"_"+"poseInUtmTiles",robotSender.callBackTwist,10)

    #while rclpy.ok():
    rclpy.spin(node)

    return
 
    

if __name__ == '__main__':
    main()
    