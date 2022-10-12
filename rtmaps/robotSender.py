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
from robotDescription import *
from ServerClient import *

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
		
		asyncio.run(self.connect())
		
	async def connect(self):
		"""connection au server"""
		self.client = Client(url=self.url)
		if self.ENCRYPT:
			await client.set_security(
				SecurityPolicyBasic256Sha256,
				certificate=self.certificate,
				private_key=self.private_key,
				#server_certificate="certificate-example.der"
				server_certificate=self.certificate #"vincent/my_cert.der"server_certificate="vincent/my_cert.der"
				#mode=ua.MessageSecurityMode.SignAndEncrypt
			)
			#mode=ua.MessageSecurityMode.SignAndEncrypt
	
	async def process(self):
		async with self.client:
			#objects = client.nodes.objects
			
			idx = await self.client.get_namespace_index(self.namespace)
			print ("idx="+str(idx))
			
			myRobotClient= MyRobotClient(self.client,idx,self.currentRobotDescription)
			await myRobotClient.initialize()
			robotGet=await myRobotClient.readRobot()
			
			import time
			#simple call to update a value
			variabluesToUpdate =robotGet.setPosition(time.time(),-1,[11.0,12.0,13.0,0.0,0.0,1.5])#ts, mapid, txyz rxyz
			await myRobotClient.writeRobot(variabluesToUpdate)#force the update of only variables usefulls
			
			robotGet=await myRobotClient.readRobot()
			
			#await self.client.disconnect()
			#print ("finish")
			
	async def task(self,loop):
	
		#url = "opc.tcp://admin@127.0.0.1:4840/freeopcua/server/"
		client = Client(url=self.url)
		#client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") 
		if self.ENCRYPT:
			await client.set_security(
				SecurityPolicyBasic256Sha256,
				certificate=self.certificate,
				private_key=self.private_key,
				#server_certificate="certificate-example.der"
				server_certificate=self.certificate #"vincent/my_cert.der"server_certificate="vincent/my_cert.der"
				#mode=ua.MessageSecurityMode.SignAndEncrypt
			)
			#mode=ua.MessageSecurityMode.SignAndEncrypt
		
		async with client:
			#objects = client.nodes.objects
			
			idx = await client.get_namespace_index(self.namespace)
			print ("idx="+str(idx))
			
			myRobotClient= MyRobotClient(client,idx,self.currentRobotDescription)
			await myRobotClient.initialize()
			robotGet=await myRobotClient.readRobot()
			
			import time
			#simple call to update a value
			variabluesToUpdate =robotGet.setPosition(time.time(),-1,[11.0,12.0,13.0,0.0,0.0,1.5])#ts, mapid, txyz rxyz
			await myRobotClient.writeRobot(variabluesToUpdate)#force the update of only variables usefulls
			
			robotGet=await myRobotClient.readRobot()
			
			await client.disconnect()
			print ("finish")
# Core() is called every time you have a new input
	def Core(self):
		
		print ("sys.path="+str(sys.path))
		timeStamp=self.inputs["inputPosition_MapID_latLongAltRPYinrad"].ioelt.ts
		data=self.inputs["inputPosition_MapID_latLongAltRPYinrad"].ioelt.data
		#print ("timeStamp="+str(timeStamp))
		#print ("data="+str(data))
		asyncio.run(self.process())
		
		#loop.run_until_complete(task(loop))
		#loop.close()
		

# Death() will be called once at diagram execution shutdown
	def Death(self):
		pass
