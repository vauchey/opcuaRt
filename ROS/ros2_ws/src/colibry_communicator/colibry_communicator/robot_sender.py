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

import asyncio
import logging
import sys
import os
import time
import asyncua

#pip install utm
import utm


logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("asyncua")

DEBUG=True
#rostopic echo rosout

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
   



class RobotSender:
    def __init__(self,node):
        

        #myPrint("!!!!!!!!!!!!!!!!!!sys.path="+str(sys.path))

        #get parameters
        self.node = node
        self.robotName=getParameter(self.node,"robotName")
        self.url=getParameter(self.node,"url")
        self.namespace=getParameter(self.node,"namespace")
        self.certificate=getParameter(self.node,"certificate")
        self.private_key=getParameter(self.node,"private_key")
        self.ENCRYPT=getParameter(self.node,"ENCRYPT")

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


        self.clientGesture = ClientGesture(self.url,self.namespace,self.certificate,self.private_key,self.ENCRYPT,currentRobotDescription)
        asyncio.run(self.clientGesture.connect())#do a connection

        
        #initiallisation des topics out
        #self.pubVelocity = rclpy.Publisher(getCurrentFileName()+"_"+'cmd_vel', Twist, queue_size=10)
        #self.pubVelocity = rclpy.Publisher(getCurrentFileName()+"_"+'cmd_vel', Twist, queue_size=10)
        self.pubVelocity = self.node.create_publisher(Twist, getCurrentFileName()+"_"+'cmd_vel'  , 10)
        pass

    def process(self):
        #myPrint ("process call")
        #send a new position only if neede
        #asyncio.run(self.clientGesture.setPosition(timeStamp,-1,data))#run a processing

        #envoit d'informations au server
        if  self.newData == True:
            myPrint ("!will send new Dataaaaaaaaaaaaaaa")
            asyncio.run(self.clientGesture.setPosition(self.timeStamp,-1,self.data))#run a processing
            myPrint ("!send new Dataaaaaaaaaaaaaaa")
            self.newData=False

        #recuperation d'infos du robot
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
   

    def callBackNavSatFix(self,navSatFix):
        #myPrint ("ttttttcallBackNavSatFix(navSatFix)")

        #try to get zone number and letter
        try:
            utmX, utmY, zoneNumber, zoneLetter = utm.from_latlon( navSatFix.latitude, navSatFix.longitude )
            self.zoneNumber=zoneNumber
            self.zoneLetter=zoneLetter
        except:
            pass
        #
        self.utmx= utmX
        self.utmy= utmY
        self.altitude= navSatFix.altitude
        
        self.sendPose()



    def callBackTwist(self,twist):
        #myPrint ("yyyyyyycallBackTwist(Twist)")
        self.utmx= twist.linear.x
        self.utmy= twist.linear.y
        self.altitude= twist.linear.z
        self.roll= twist.angular.x
        self.pitch= twist.angular.y
        self.yaw= twist.angular.z

        self.sendPose()

       


    def callBackImu(self,imu):
        #myPrint ("callBackImu(Imu)")

        quat=[imu.orientation.w,imu.orientation.x,imu.orientation.y,imu.orientation.z]
        [roll, pitch, yaw]= R.from_quat(quat).as_euler("ZYX",degrees=False)
        self.roll=roll
        self.pitch=pitch
        self.yaw=(math.pi/2.0)-yaw

        self.sendPose()


    def sendPose(self):
        """send current robot pose to server"""

        """
        myPrint ("self.utmx :::"+str(self.utmx))
        myPrint ("self.utmy :::"+str(self.utmy))
        myPrint ("self.altitude :::"+str(self.altitude))
        myPrint ("self.zoneNumber :::"+str(self.zoneNumber))
        myPrint ("self.zoneLetter :::"+str(self.zoneLetter))
        myPrint ("self.roll :::"+str(self.roll))
        myPrint ("self.pitch :::"+str(self.pitch))
        myPrint ("self.yaw :::"+str(self.yaw))
        """


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
            self.data=[lati,longi, self.altitude,self.roll, self.pitch, self.yaw]
            myPrint ("send to server !!!!!!!!!!"+str(self.data))
            self.newData=True
            #asyncio.run(self.clientGesture.setPosition(timeStamp,-1,data))#run a processing

            #asyncio.run(self.clientGesture.readRobot())
            #print ("robotGet.ts_map_id_posexyzrxryrz="+str(self.clientGesture.currentRobotDescription.ts_map_id_posexyzrxryrz))
		
"""
import rclpy
rclpy.init()
node = rclpy.create_node("robot_sender")
rate = node.create_rate(10)
rate = node.create_rate(10, node.get_clock())
rate.sleep()
#https://www.programcreek.com/python/example/118511/rclpy.ok
"""

def main(args=None):
    #rclpy.init_node('my_broadcaster')
    rclpy.init(args=args)
    node = rclpy.create_node("robot_sender")
    #node.get_parameter("FREQUENCY")
    robotSender = RobotSender(node)

    
    

    #create several callback
    #rclpy.Subscriber(getCurrentFileName()+"_"+"navSatFix", NavSatFix, robotSender.callBackNavSatFix)
    #rclpy.Subscriber(getCurrentFileName()+"_"+"imu", Imu, robotSender.callBackImu)
    #rclpy.Subscriber(getCurrentFileName()+"_"+"poseInUtmTiles", Twist, robotSender.callBackTwist)

    node.create_subscription(NavSatFix, getCurrentFileName()+"_"+"navSatFix",robotSender.callBackNavSatFix,10)
    node.create_subscription(Imu, getCurrentFileName()+"_"+"imu",robotSender.callBackImu,10)
    node.create_subscription(Twist, getCurrentFileName()+"_"+"poseInUtmTiles",robotSender.callBackTwist,10)


    #stay reactive

    robot_sender_FREQUENCY=getParameter(node,"FREQUENCY")
    myPrint("robot_sender_FREQUENCY="+str(robot_sender_FREQUENCY))
    #rate = node.create_rate(robot_sender_FREQUENCY, node.get_clock())
    rate = node.create_rate(robot_sender_FREQUENCY)
    #rate = rclpy.Rate(robot_sender_FREQUENCY)  # 5hz
    while not rate._is_shutdown:#rclpy.ok()
        #while not rclpy.is_shutdown():
        myPrint ("will process callaaaaaa")
        robotSender.process()
        """
        if  robotSender.newData == True:
            asyncio.run(robotSender.clientGesture.setPosition(robotSender.timeStamp,-1,robotSender.data))#run a processing
            print ("!send new Dataaaaaaaaaaaaaaa")
            robotSender.newData=False
      
        """
        """
        asyncio.run(robotSender.clientGesture.readRobot())
        print ("robotGet.ts_map_id_posexyzrxryrz="+str(robotSender.clientGesture.currentRobotDescription.ts_map_id_posexyzrxryrz))
        """
        rate.sleep()
        

    #rclpy.spin()
    

    
    
    

if __name__ == '__main__':
    main()
