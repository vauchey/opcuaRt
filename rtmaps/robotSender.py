#This is a template code. Please save it in a proper .py file.
import rtmaps.types
import numpy as np
import rtmaps.core as rt 
import rtmaps.reading_policy 
from rtmaps.base_component import BaseComponent # base class 

import asyncio
import logging
import sys
import os

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


# Python class that will be called from RTMaps.
class rtmaps_python(BaseComponent):
	def __init__(self):
		BaseComponent.__init__(self) # call base class constructor

	def Dynamic(self):
		self.add_input("inputPosition_MapID_latLongAltRPYinrad", rtmaps.types.ANY) # define input
		self.add_output("enabled_vLongiwantedMBysedVrotWantedRadBySec", rtmaps.types.AUTO)
		self.add_output("ouput_Mapid_Position", rtmaps.types.AUTO)
		listOfName = listNames()
		
		#genere automatiquement la liste rtmaps
		listRtMaps=str(len(listOfName))+"|0|"+"|".join(str(val) for val in listOfName)
		self.add_property("robotName",listRtMaps, rtmaps.types.ENUM)
		
		
		
		self.add_property("ENCRYPT",True)
		self.add_property("url","opc.tcp://127.0.0.1:4840/freeopcua/server/")
		self.add_property("namespace","http://esigelec.ddns.net")
		
		self.add_property("certificate", "vincent/my_cert.der", rtmaps.types.FILE)
		self.add_property("private_key", "vincent/my_private_key.pem", rtmaps.types.FILE)
		
		#lecture des property
		self.ENCRYPT=self.properties["ENCRYPT"].data
		self.url=self.properties["url"].data
		self.namespace=self.properties["namespace"].data
		self.certificate=self.properties["certificate"].data
		self.private_key=self.properties["private_key"].data
		
		robotName = listOfName[ self.properties["robotName"].data ]
		#print ("robotName="+str(robotName))
		self.currentRobotDescription = getCurrentRobotName(robotName)
		#print (sys.path)
# Birth() will be called once at diagram execution startup

	def Birth(self):
		print("Python Birth")
		assert (self.currentRobotDescription!=None, "robot not find")#verification que le robot existe
		
		self._timeStamp=-1
		
		self.clientGesture = ClientGesture(self.url,self.namespace,self.certificate,self.private_key,self.ENCRYPT,self.currentRobotDescription)
		asyncio.run(self.clientGesture.connect())#do a connection
		
		#temp
		"""self.url = "opc.tcp://127.0.0.1:4840/freeopcua/server/"
		self.namespace = "http://esigelec.ddns.net"#namespace
		"""
		#USER certificate and key
		"""
		self.certificate="D:/data/apresBackup/COLIBRY/opcuaRT/opcuaRt/client/vincent/my_cert.der"#f"vincent/my_cert.der"
		self.private_key="D:/data/apresBackup/COLIBRY/opcuaRT/opcuaRt/client/vincent/my_private_key.pem"#f"vincent/my_private_key.pem"


		self.clientGesture = ClientGesture(self.url,self.namespace,self.certificate,self.private_key,self.ENCRYPT,self.currentRobotDescription)
		#asyncio.run(self.clientGesture.connect())#do a connection
		
		clientGesture = ClientGesture(self.url,self.namespace,self.certificate,self.private_key,self.ENCRYPT,self.currentRobotDescription)
		asyncio.run(clientGesture.connect())#do a connection
		import time
		timeStamp=time.time()
		data=[1.0,2.0,3.0,4.0,5.0,6.0]
		asyncio.run(clientGesture.setPosition(timeStamp,-1,data))
		"""

# Core() is called every time you have a new input
	def Core(self):
		
		print ("sys.path="+str(sys.path))
		try :
			timeStamp=self.inputs["inputPosition_MapID_latLongAltRPYinrad"].ioelt.ts
			data=self.inputs["inputPosition_MapID_latLongAltRPYinrad"].ioelt.data
		except:
			timeStamp=-1
			pass
			
		#send new pose only if need
		if ((timeStamp != self._timeStamp) and (timeStamp!=-1)):
			self._timeStamp=timeStamp
			asyncio.run(self.clientGesture.setPosition(timeStamp,-1,data[1:]))#run a processing
			
		#get information about robot
		asyncio.run(self.clientGesture.readRobot())
		print ("robotGet.ts_map_id_posexyzrxryrz="+str(self.clientGesture.currentRobotDescription.ts_map_id_posexyzrxryrz))
		
		

		#sortie de la commande venant du server
		wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec=self.clientGesture.currentRobotDescription.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec
		enabled_vLongiwantedMBysedVrotWantedRadBySec = rtmaps.types.Ioelt()
		enabled_vLongiwantedMBysedVrotWantedRadBySec.data=[wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec[1],wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec[2],wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec[3]]
		enabled_vLongiwantedMBysedVrotWantedRadBySec.vector_size = len(enabled_vLongiwantedMBysedVrotWantedRadBySec.data)
		enabled_vLongiwantedMBysedVrotWantedRadBySec.ts = wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec[0]#rt.current_time()
		self.outputs["enabled_vLongiwantedMBysedVrotWantedRadBySec"].write(enabled_vLongiwantedMBysedVrotWantedRadBySec)
					
					
					
		#send pose
		currentPose = rtmaps.types.Ioelt()
		ts_map_id_posexyzrxryrz=self.clientGesture.currentRobotDescription.ts_map_id_posexyzrxryrz
		print ("ts_map_id_posexyzrxryrz.shape="+str(len(ts_map_id_posexyzrxryrz)))
		currentPose.data=[ts_map_id_posexyzrxryrz[1],ts_map_id_posexyzrxryrz[2],ts_map_id_posexyzrxryrz[3],ts_map_id_posexyzrxryrz[4],ts_map_id_posexyzrxryrz[5],ts_map_id_posexyzrxryrz[6],ts_map_id_posexyzrxryrz[7]]
		currentPose.vector_size = len(currentPose.data)
		currentPose.ts = timeStamp
		self.outputs["ouput_Mapid_Position"].write(currentPose)
		"""lf.ts_map_id_posexyzrxryrz = [0.0, -1.0,1000.0, 1000.0,1000.0,1000.0,1000.0,1000.0]#pose in meters
		self.stdev_ts_map_id_posexyzrxryrz = [0.0, 1000.0, 1000.0,1000.0,1000.0,1000.0,1000.0]
		
		self.ts_map_id_posexyzrxryrz_target = [0.0, -1.0,1000.0, 1000.0,1000.0,1000.0,1000.0,1000.0]#target
		
		self.robotStatus=0.0 #enumt do describe the status
		self.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec=[0.0,0.0,0.0,0.0]"""
		#print ("timeStamp="+str(timeStamp))
		#print ("data="+str(data))
		
		
		#loop.run_until_complete(task(loop))
		#loop.close()
		

# Death() will be called once at diagram execution shutdown
	def Death(self):
		pass
