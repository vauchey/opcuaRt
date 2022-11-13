#This is a template code. Please save it in a proper .py file.
import rtmaps.types
import numpy as np
import rtmaps.core as rt 
import rtmaps.reading_policy 
from rtmaps.base_component import BaseComponent # base class 
import threading

import asyncio
import logging
import sys
import os


import subprocess
#sys.path.insert(0, "..")


sys.path.append( os.path.abspath(sys.path[0]+"/../"))
#os.chdir(os.path.abspath(sys.path[0]+"/../"))

#add the same sys path than anaconda
"""sys.path.append('C:\\ProgramData\\Anaconda3\\Scripts')
sys.path.append('C:\\ProgramData\\Anaconda3\\python37.zip')
sys.path.append('C:\\ProgramData\\Anaconda3\\DLLs')
sys.path.append('C:\\ProgramData\\Anaconda3\\lib')
sys.path.append('C:\\ProgramData\\Anaconda3')
sys.path.append('C:\\Users\\admin\\AppData\\Roaming\\Python\\Python37\\site-packages')
sys.path.append('C:\\ProgramData\\Anaconda3\\lib\\site-packages\\locket-0.2.1-py3.7.egg')
sys.path.append('C:\\ProgramData\\Anaconda3\\lib\\site-packages\\win32')
sys.path.append('C:\\ProgramData\\Anaconda3\\lib\\site-packages\\win32\\lib')
sys.path.append('C:\\ProgramData\\Anaconda3\\lib\\site-packages\\Pythonwin')
sys.path.append('C:\\ProgramData\\Anaconda3\\lib\\site-packages\\IPython\\extensions')
sys.path.append('C:\\Users\\admin\\.ipython')
"""


#import to know the robots
from robotDescription import *
#import to do client gesture
from ClientGesture import *


import multiprocessing
"""
pip install asyncua
#Ubuntu:
#apt install python-opcua        # Library
#apt install python-opcua-tools  # Command-line tools
"""
from asyncua import Client, Node, ua
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256

#logging.basicConfig(level=logging.INFO)
#_logger = logging.getLogger("asyncua")
import time
#create au child class of ClientGesture and redefine specifics value for rtmaps
class ClientGestureRtMaps(ClientGesture):
	def __init__(self,url,namespace, certificate, private_key,ENCRYPT,currentRobotDescription):
		#call parent constructor
		super().__init__(url,namespace, certificate, private_key,ENCRYPT,currentRobotDescription)
		
	def isDying(self):
		return rt.is_dying()
		
		
	
	
import os


# Python class that will be called from RTMaps.
class rtmaps_python(BaseComponent):
	def __init__(self):
		BaseComponent.__init__(self) # call base class constructor


	
		
	def Dynamic(self):
		self.add_input("inputPosition_MapID_latLongAltRPYinrad", rtmaps.types.ANY) # define input
		self.add_input("inputMove_Vlong_Vrot", rtmaps.types.ANY) # define input
		self.add_output("enabled_vLongiwantedMBysedVrotWantedRadBySec", rtmaps.types.AUTO)#rtmaps.types.AUTO
		self.add_output("ouput_Mapid_Position", rtmaps.types.AUTO)
		listOfName = listNames()
		
		#genere automatiquement la liste rtmaps
		listRtMaps=str(len(listOfName))+"|0|"+"|".join(str(val) for val in listOfName)
		self.add_property("robotName",listRtMaps, rtmaps.types.ENUM)
		#self.add_property("UDP_PORT",5006, )
		
		self.add_property("communicationPeriodInS",0.05)
		
		#self.add_property("ENCRYPT",True)
		#self.add_property("url","opc.tcp://127.0.0.1:4840/freeopcua/server/")
		#self.add_property("namespace","http://esigelec.ddns.net")
		
		#self.add_property("certificate", "vincent/my_cert.der", rtmaps.types.FILE)
		#self.add_property("private_key", "vincent/my_private_key.pem", rtmaps.types.FILE)
		
		#lecture des property
		self.ENCRYPT=False#self.properties["ENCRYPT"].data
		self.url=""#self.properties["url"].data
		self.namespace=""#self.properties["namespace"].data
		self.certificate=""#self.properties["certificate"].data
		self.private_key=""#self.properties["private_key"].data
		
		self.robotName = listOfName[ self.properties["robotName"].data ]
		#print ("self.robotName="+str(self.robotName))
		self.currentRobotDescription = getCurrentRobotName(self.robotName)
		self.communicationPeriodInS = self.properties["communicationPeriodInS"].data
		#self.UDP_PORT = self.properties["UDP_PORT"].data
		
		self.currentRobotIndex = getCurrentRobotNameIndex(self.robotName)
		
		#print (sys.path)
# Birth() will be called once at diagram execution startup

	def Birth(self):
		#print (dir(self))
		#assert(1==2)
		print("Python Birth")
		assert (self.currentRobotDescription!=None, "robot not find")#verification que le robot existe
		assert (self.currentRobotIndex!=-1, "robot index not find")#verification que le robot existe
		
		self._timeStamp=-1
		self._timeStampSpeedWanted=-1
		
		UDP_PORT_BEGIN=5000

		self.clientGesture = ClientGestureRtMaps(self.url,self.namespace,self.certificate,self.private_key,self.ENCRYPT,self.currentRobotDescription)
		self.clientGesture.createSubprocessAndRunIt(self.communicationPeriodInS,self.robotName,UDP_PORT_BEGIN+self.currentRobotIndex,True)#juste create a socket
			
		
# Core() is called every time you have a new input
	def Core(self):
		#print ("!!!!!!!!!!!!!!!!RobotSender Core")
		
		#check position
		try :
			timeStamp=self.inputs["inputPosition_MapID_latLongAltRPYinrad"].ioelt.ts
			data=self.inputs["inputPosition_MapID_latLongAltRPYinrad"].ioelt.data
		except:
			timeStamp=-1
			pass
		
		if ((timeStamp != self._timeStamp) and (timeStamp!=-1)):
			self._timeStamp=timeStamp
			#print ("self.clientGesture.getIsReady()="+str(self.clientGesture.getIsReady()))
			#if self.clientGesture.getIsReady():
			#print ("send setPosition "+str(list(data[1:])))
			self.clientGesture.setPosition(timeStamp,-1,list(data[1:]))#only basic type allowed
				
		
		#check commands
		try :
			timeStampSpeedWanted=self.inputs["inputMove_Vlong_Vrot"].ioelt.ts
			inputMove_Vlong_Vrotdata=self.inputs["inputMove_Vlong_Vrot"].ioelt.data
		except :
			timeStampSpeedWanted=-1
			
		if ((timeStampSpeedWanted != self._timeStampSpeedWanted) and (timeStampSpeedWanted!=-1)):
			self._timeStampSpeedWanted=timeStampSpeedWanted
			#print ("send moveRobot")
			self.clientGesture.moveRobot(timeStampSpeedWanted,inputMove_Vlong_Vrotdata[0],inputMove_Vlong_Vrotdata[1],inputMove_Vlong_Vrotdata[2])
		#disable
		"""
		asyncio.run(self.clientGesture.moveRobot( timeStamp,False,self.vLongi,self.vRot) )#run a processing
			else:
				#control the robot
				asyncio.run(self.clientGesture.moveRobot( timeStamp,True,self.vLongi,self.vRot) )#run a processing
		"""
		
		#print (self.subp.stdout.read(10))
		
		
		result =self.clientGesture.readVariables()
		#print ("reult:"+str(result))
		if result:
		
			#print ("send vlongi wanted")
			#send vlongi wanted
			wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec=self.clientGesture.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec
			enabled_vLongiwantedMBysedVrotWantedRadBySec = rtmaps.types.Ioelt()
			enabled_vLongiwantedMBysedVrotWantedRadBySec.data=[wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec[1],wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec[2],wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec[3]]
			enabled_vLongiwantedMBysedVrotWantedRadBySec.vector_size = len(enabled_vLongiwantedMBysedVrotWantedRadBySec.data)
			enabled_vLongiwantedMBysedVrotWantedRadBySec.ts = rt.current_time()#wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec[0]#rt.current_time()
			self.outputs["enabled_vLongiwantedMBysedVrotWantedRadBySec"].write(enabled_vLongiwantedMBysedVrotWantedRadBySec)
			print ("send vlongi wanted done")
			
			#send pose
			#print ("send pose")
			currentPose = rtmaps.types.Ioelt()
			ts_map_id_posexyzrxryrz=self.clientGesture.ts_map_id_posexyzrxryrz
			print ("ts_map_id_posexyzrxryrz.shape="+str(len(ts_map_id_posexyzrxryrz)))
			currentPose.data=[ts_map_id_posexyzrxryrz[1],ts_map_id_posexyzrxryrz[2],ts_map_id_posexyzrxryrz[3],ts_map_id_posexyzrxryrz[4],ts_map_id_posexyzrxryrz[5],ts_map_id_posexyzrxryrz[6],ts_map_id_posexyzrxryrz[7]]
			currentPose.vector_size = len(currentPose.data)
			currentPose.ts = rt.current_time()#timeStamp
			self.outputs["ouput_Mapid_Position"].write(currentPose)
			#print ("send pose done")
			
		
		
		
		
		
# Death() will be called once at diagram execution shutdown
	def Death(self):
		#print ("calll deathhhhhhhhhhh")
		#print ("stopProcess")
		#self.clientGesture.stopProcess()
		pass
