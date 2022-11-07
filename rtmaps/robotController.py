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

	"""
	async def processTask(self):
		""" thread asyncio permetant de communiquer avec le server"""
		
		clientGesture = ClientGesture(self.url,self.namespace,self.certificate,self.private_key,self.ENCRYPT,self.currentRobotDescription)
		await clientGesture.connect()
	"""
		
	def Dynamic(self):
		
		self.add_input("joystick", rtmaps.types.ANY) # define input[0 is -la, 1 is -ling, 2, is deadman]
		self.add_input("buttons", rtmaps.types.ANY) # define input[0 is up, 1 is downs]
		self.add_output("robotOut", rtmaps.types.AUTO,buffer_size=512)
		#self.add_input("inputVLongiMbysecVrotradbysec", rtmaps.types.ANY) # define input
		
		#listOfName = listNames()
		
		#genere automatiquement la liste rtmaps
		#listRtMaps=str(len(listOfName))+"|0|"+"|".join(str(val) for val in listOfName)
		#self.add_property("robotName",listRtMaps, rtmaps.types.ENUM)
		
		
		
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
		
		#robotName = listOfName[ self.properties["robotName"].data ]
		#print ("robotName="+str(robotName))
		#self.currentRobotDescription = getCurrentRobotName(robotName)
		#print (sys.path)
# Birth() will be called once at diagram execution startup

	def Birth(self):
		print("Python Birth")
		
		
		self._timeStamp=-1
		
		#list all name
		self.listOfName = listNames()
		
		self.currentRobotDescriptionList=[]
		for names in self.listOfName:
			self.currentRobotDescriptionList.append( getCurrentRobotName(names) )
		
		assert (len(self.currentRobotDescriptionList)>0,"not robots to control")
		
		self.currentRobot=0
		self.clientGesture = ClientGesture(self.url,self.namespace,self.certificate,self.private_key,self.ENCRYPT,self.currentRobotDescriptionList[self.currentRobot])
		asyncio.run(self.clientGesture.connect())#do a connection
		##asyncio.run(self.clientGesture.getCurrentRobot())
		
		self.vRot =0.0
		self.vLongi=0.0
		
# Core() is called every time you have a new input
	def Core(self):
		if( self.input_that_answered==0):
			timeStamp=self.inputs["joystick"].ioelt.ts
			joystick = self.inputs["joystick"].ioelt.data
			self.vRot= np.radians( (-joystick[0]/1000.0) * 15.0 ) # at full will turn of 45 deg by seg
			self.vLongi= -joystick[1]/1000.0#1 Mbsec max
			#raz si pas d'homme mort
			if (joystick[2] < 500):
				self.vRot=0.0
				self.vLongi=0.0
				#disable
				asyncio.run(self.clientGesture.moveRobot( timeStamp,False,self.vLongi,self.vRot) )#run a processing
			else:
				#control the robot
				asyncio.run(self.clientGesture.moveRobot( timeStamp,True,self.vLongi,self.vRot) )#run a processing
				
				
			#send vlongi
			
		elif( self.input_that_answered==1):
			timeStamp  =self.inputs["buttons"].ioelt.ts
			
			#print("vectorsize="+str(self.inputs["buttons"].ioelt.vector_size))
			if self.inputs["buttons"].ioelt.vector_size > 0:
				buttonRead = self.inputs["buttons"].ioelt.data
				if (buttonRead == 0):
					#send vlongi to 0 to current robot
					asyncio.run(self.clientGesture.moveRobot( timeStamp,False,0.0,0.0) )#stop it
					
					#change robot
					self.currentRobot-=1
					if(self.currentRobot <0):
						self.currentRobot=len(self.listOfName)-1
					self.clientGesture.currentRobotDescription = self.currentRobotDescriptionList[self.currentRobot]#update the robots informations
					asyncio.run(self.clientGesture.getCurrentRobot())#force to connect to the good robot
					#re init
					asyncio.run(self.clientGesture.moveRobot( timeStamp,False,0.0,0.0) )#stop it
					
				elif (buttonRead == 3):
					#send vlongi to 0 to current robot
					
					#change robot
					self.currentRobot+=1
					self.currentRobot=self.currentRobot%len(self.listOfName)
					
					self.clientGesture.currentRobotDescription = self.currentRobotDescriptionList[self.currentRobot]#update the robots informations
					asyncio.run(self.clientGesture.getCurrentRobot())#force to connect to the good robot
					#print ("rboto selected !!!!!!!!!!="+str(self.clientGesture.currentRobotDescription.robotName))
					#re init
					asyncio.run(self.clientGesture.moveRobot( timeStamp,False,0.0,0.0) )#stop it
					
		
		robotOutOuput = rtmaps.types.Ioelt()
		robotOutOuput.data=self.listOfName[self.currentRobot]+"\n"
		#robotOutOuput.vector_size = len(enabled_vLongiwantedMBysedVrotWantedRadBySec.data)
		robotOutOuput.ts = rt.current_time()
		self.outputs["robotOut"].write(robotOutOuput)
		
		"""try :
			timeStamp=self.inputs["inputPosition_MapID_latLongAltRPYinrad"].ioelt.ts
			data=self.inputs["inputPosition_MapID_latLongAltRPYinrad"].ioelt.data
		except:
			pass
			
		#send new pose only if need
		if timeStamp != self._timeStamp:
			self._timeStamp=timeStamp
			asyncio.run(self.clientGesture.setPosition(timeStamp,-1,data))#run a processing
			
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
		"""		
					
		
		

# Death() will be called once at diagram execution shutdown
	def Death(self):
		pass
