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


# Python class that will be called from RTMaps.
class rtmaps_python(BaseComponent):
	def __init__(self):
		BaseComponent.__init__(self) # call base class constructor

	def Dynamic(self):
		self.add_input("inputPosition_MapID_latLongAltRPYinrad", rtmaps.types.ANY) # define input
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

# Birth() will be called once at diagram execution startup

	def Birth(self):
		print("Python Birth")
		assert (self.currentRobotDescription!=None, "robot not find")#verification que le robot existe
		
		
		"""
		loop = asyncio.get_event_loop()
		loop.set_debug(True)
		loop.run_until_complete(self.task(loop))
		loop.close()
		"""
		self.clientGesture = ClientGesture(self.url,self.namespace,self.certificate,self.private_key,self.ENCRYPT,self.currentRobotDescription)
		asyncio.run(self.clientGesture.connect())#do a connection
		
		

# Core() is called every time you have a new input
	def Core(self):
		
		print ("sys.path="+str(sys.path))
		timeStamp=self.inputs["inputPosition_MapID_latLongAltRPYinrad"].ioelt.ts
		data=self.inputs["inputPosition_MapID_latLongAltRPYinrad"].ioelt.data
		#print ("timeStamp="+str(timeStamp))
		#print ("data="+str(data))
		asyncio.run(self.clientGesture.process(timeStamp,data))#run a processing
		
		#loop.run_until_complete(task(loop))
		#loop.close()
		

# Death() will be called once at diagram execution shutdown
	def Death(self):
		pass
