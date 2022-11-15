#! /usr/bin/env python3




import rospy
from rospy import Time 



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
        #rospy.loginfo(msg)
        print(msg)

print ("sys.path[0]="+str(sys.path[0]))
sys.path.append( os.path.abspath(sys.path[0]+"/../../../../../"))
#sys.path.append( os.path.abspath(sys.path[0]+"/../../../../../../"))#for ros2 arch

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

class ClientGestureROS(ClientGesture):
    def __init__(self,url,namespace, certificate, private_key,ENCRYPT,currentRobotDescription):
        super().__init__(url,namespace, certificate, private_key,ENCRYPT,currentRobotDescription)



    def isDying(self):
        """function to redefine for ros or rtmaps, for example on rtmaps it will be rt.is_dying()"""
        if rospy.is_shutdown():
            return True
        else:
            return False



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
    def __init__(self):
        

        #myPrint("!!!!!!!!!!!!!!!!!!sys.path="+str(sys.path))
       
        #get parameters

        self.robotName=getParameter("robotName")
        self.url=getParameter("url")
        self.namespace=getParameter("namespace")
        self.certificate=getParameter("certificate")
        self.private_key=getParameter("private_key")
        self.ENCRYPT=getParameter("ENCRYPT")
        self.robot_sender_FREQUENCY=getParameter("FREQUENCY")
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
            self.latitude=getParameter("defaultLatitude")
        except :
            self.latitude=None

        try :
            self.lontitude=getParameter("defaultLongitude")
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


        #initiallisation des topics out
        #self.pubVelocity = rclpy.Publisher(getCurrentFileName()+"_"+'cmd_vel', Twist, queue_size=10)
        #self.pubVelocity = rclpy.Publisher(getCurrentFileName()+"_"+'cmd_vel', Twist, queue_size=10)
        self.pubVelocity = rospy.Publisher(getCurrentFileName()+"_"+'cmd_vel', Twist, queue_size=10)
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


            self.timeStamp=(rospy.Time.now().to_nsec()/1000)#time us us
            self.data=[lati,longi, self.altitude,self.roll, self.pitch, self.yaw]#must be a list
            myPrint ("send to server !!!!!!!!!!"+str(self.data))
            self.clientGesture.setPosition(self.timeStamp,-1,self.data)

def main():
    
    #rclpy.init(args=args)
    rospy.init_node('my_broadcaster')#node = rclpy.create_node("robot_sender")
    robotSender = RobotSender()


    rospy.Subscriber(getCurrentFileName()+"_"+"navSatFix", NavSatFix, robotSender.callBackNavSatFix)
    rospy.Subscriber(getCurrentFileName()+"_"+"imu", Imu, robotSender.callBackImu)
    rospy.Subscriber(getCurrentFileName()+"_"+"poseInUtmTiles", Twist, robotSender.callBackTwist)
   
    rospy.spin()
    

    
    
    

if __name__ == '__main__':
    main()
