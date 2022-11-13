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


# Python class that will be called from RTMaps.
class rtmaps_python(BaseComponent):
	def __init__(self):
		BaseComponent.__init__(self) # call base class constructor

		
		
	def Dynamic(self):
		
		self.add_input("joystick", rtmaps.types.ANY) # define input[0 is -la, 1 is -ling, 2, is deadman]
		self.add_input("buttons", rtmaps.types.ANY) # define input[0 is up, 1 is downs]
		
		self.listOfName = listNames()
		
		self.add_output("robotId", rtmaps.types.AUTO)
		
		self.ouputNames=[]
		for i in range(len(self.listOfName)):
			self.ouputNames.append( "robotOut"+str(self.listOfName[i]).replace("-","_").replace("(","_").replace(")","_") )
			self.add_output(self.ouputNames[i], rtmaps.types.AUTO,buffer_size=512)
			
		
		
	
		#self.add_input("inputVLongiMbysecVrotradbysec", rtmaps.types.ANY) # define input
		
		#listOfName = listNames()
		
		#genere automatiquement la liste rtmaps
		#listRtMaps=str(len(listOfName))+"|0|"+"|".join(str(val) for val in listOfName)
		#self.add_property("robotName",listRtMaps, rtmaps.types.ENUM)
		
		
		
	
		
		#robotName = listOfName[ self.properties["robotName"].data ]
		#print ("robotName="+str(robotName))
		#self.currentRobotDescription = getCurrentRobotName(robotName)
		#print (sys.path)
# Birth() will be called once at diagram execution startup

	def Birth(self):
		print("Python Birth")
		
	
		self.currentRobot=0

		self.vRot =0.0
		self.vLongi=0.0
		
# Core() is called every time you have a new input
	def Core(self):
		pass
		
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
				self.controlRobot(timeStamp,False,self.vLongi,self.vRot)
				#asyncio.run(self.clientGesture.moveRobot( timeStamp,False,self.vLongi,self.vRot) )#run a processing
			else:
				#control the robot
				self.controlRobot(timeStamp,True,self.vLongi,self.vRot)
				#asyncio.run(self.clientGesture.moveRobot( timeStamp,True,self.vLongi,self.vRot) )#run a processing
				
				
			#send vlongi
			
		elif( self.input_that_answered==1):
			timeStamp  =self.inputs["buttons"].ioelt.ts
			
			#print("vectorsize="+str(self.inputs["buttons"].ioelt.vector_size))
			if self.inputs["buttons"].ioelt.vector_size > 0:
				buttonRead = self.inputs["buttons"].ioelt.data
				if (buttonRead == 0):
					#send vlongi to 0 to current robot
					self.controlRobot(timeStamp,False,0.0,0.0)
					#asyncio.run(self.clientGesture.moveRobot( timeStamp,False,0.0,0.0) )#stop it
					
					#change robot
					self.currentRobot-=1
					if(self.currentRobot <0):
						self.currentRobot=len(self.listOfName)-1
					self.controlRobot(timeStamp,False,0.0,0.0)
					
					
					
				elif (buttonRead == 3):
					#send vlongi to 0 to current robot
					self.controlRobot(timeStamp,False,0.0,0.0)
					
					#change robot
					self.currentRobot+=1
					self.currentRobot=self.currentRobot%len(self.listOfName)
					
					self.controlRobot(timeStamp,False,0.0,0.0)
					
					
		
		
		robotIdOutput = rtmaps.types.Ioelt()
		robotIdOutput.data=self.currentRobot
		robotIdOutput.vector_size = 1#len(robotIdOutput.data)
		robotIdOutput.ts = timeStamp#rt.current_time()
		#print ("write to "+str(self.currentRobot))
		#print ("write to2 "+str(self.ouputNames[self.currentRobot]))
		self.outputs["robotId"].write(robotIdOutput)
		
		
	def controlRobot(self,ts,enabled, vlongi, vlat):
		
		robotOutOuput = rtmaps.types.Ioelt()
		robotOutOuput.data=[enabled,vlongi,vlat]
		robotOutOuput.vector_size = len(robotOutOuput.data)
		robotOutOuput.ts = ts#rt.current_time()
		#print ("write to "+str(self.currentRobot))
		#print ("write to2 "+str(self.ouputNames[self.currentRobot]))
		self.outputs[self.ouputNames[self.currentRobot]].write(robotOutOuput)


# Death() will be called once at diagram execution shutdown
	def Death(self):
		pass
