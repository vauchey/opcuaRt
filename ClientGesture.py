

from robotDescription import *

from asyncua import Client, Node, ua
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256




class MyRobotClient():
	
	def __init__(self,client,idx,currentRobotDescription):
		""" class de gestion d'un robot vote client"""
		self.client =client
		self.idx=idx
		self.currentRobotDescription = currentRobotDescription
		
		
		pass
		
	async def initialize(self):
		"""methode d'initialisation d'un robot cote client une fois pour toute"""		
		
		self.objects = self.client.nodes.objects
		self.robotName =  self.currentRobotDescription.__dict__["robotName"]
		print ("initialize robot :"+str(self.robotName))
		for values in  self.currentRobotDescription.__dict__.keys():
			if  values!="robotName":
				self.__dict__[values+"_child"] = await self.objects.get_child([str(self.idx)+':'+self.robotName, str(self.idx) + ':'+values])#recupere les childs (une fois pour toute)
		print ("initialize robot done:"+str(self.robotName))
		

	async def readRobot(self):
		""" lecture des infos robots et retourne l'objet robot lu"""

		#robotName =  self.currentRobotDescription.__dict__["robotName"]
		
		for values in  self.currentRobotDescription.__dict__.keys():
			if  values!="robotName":
				#child = await self.objects.get_child([str(self.idx)+':'+self.robotName, str(self.idx) + ':'+values])#recupere le child
				#self.__dict__[values]=await self.__dict__[values+"_child"].get_value()
				self.currentRobotDescription.__dict__[values]=await self.__dict__[values+"_child"].get_value()
				
		print (self.currentRobotDescription.__dict__)
		return self.currentRobotDescription
		
	async def writeRobot(self,variabluesToUpdate):
		""" send to server from a list of variabluesToUpdate, update only variables asked"""
		if variabluesToUpdate is not None:
			for variablesToUpdate in variabluesToUpdate:
				#print ("try to pupdate="+str(variablesToUpdate))
				#print ("try to pupdate2="+str(self.__dict__[variablesToUpdate+"_child"]))
				#print ("value to write="+str(self.currentRobotDescription.__dict__[variablesToUpdate]))
				await self.__dict__[variablesToUpdate+"_child"].set_value(self.currentRobotDescription.__dict__[variablesToUpdate])
			#for values in  self.currentRobotDescription.__dict__.keys():
			#if  values != "robotName":
			#		self.__dict__[values+"_child"].set_value(self.currentRobotDescription.__dict__[values])#update des valeurs
			
			

		
class ClientGesture():
	def __init__(self,url,namespace, certificate, private_key,ENCRYPT,currentRobotDescription):
		self.url=url
		self.namespace= namespace
		self.certificate=certificate
		self.private_key=private_key
		self.client=None
		self.ENCRYPT=ENCRYPT
		self.currentRobotDescription = currentRobotDescription
		
		self.robotGet=None
		
	async def getCurrentRobot(self):
		"""permet de seconnecter au bon robot, peut etre appeller depuis lexterieur en cas de changement de robot"""
		async with self.client:
			self.idx = await self.client.get_namespace_index(self.namespace)
			#print ("idx="+str(idx))
		
			#init robot
			#print ("!!!!!!!!!!!!create robot :"+str(self.currentRobotDescription.robotName))
			self.myRobotClient= MyRobotClient(self.client,self.idx,self.currentRobotDescription)
			await self.myRobotClient.initialize()
			
			
	async def connect(self):
		"""method to connect to server"""
		self.client = Client(url=self.url)
		print("called::connect")
		if self.ENCRYPT:
			print ("self.certificate ="+str(self.certificate))
			print ("self.private_key ="+str(self.private_key))
			#async with self.client:
			await self.client.set_security(
				SecurityPolicyBasic256Sha256,
				certificate=self.certificate,
				private_key=self.private_key,
				#server_certificate="certificate-example.der"
				#server_certificate=self.certificate #"vincent/my_cert.der"server_certificate="vincent/my_cert.der"
				mode=ua.MessageSecurityMode.SignAndEncrypt
			)
			#mode=ua.MessageSecurityMode.SignAndEncrypt
		#async with self.client:
		#	await self.getCurrentRobot()#
		#print("!!!!!!!!!!!!!!!!!!!!!!!!!!call self.getCurrentRobot")
		await self.getCurrentRobot()#
		
		"""
		async with self.client:
			self.idx = await self.client.get_namespace_index(self.namespace)
			#print ("idx="+str(idx))
		
			#init robot
			self.myRobotClient= MyRobotClient(self.client,self.idx,self.currentRobotDescription)
			await self.myRobotClient.initialize()
		print("!!!!!!!!!!!!!!!!!!!!!!!!!!call self.getCurrentRobot done")
		"""
		
	async def moveRobot(self, timestamp,enabled,Vlongi,Vrot):
		"""method to check connection and then send to server a movement"""
		if self.client  is None :
			print("moveRobot::connect")
			self.connect()
			
		if self.client is not None :
			async with self.client:
				"""self.myRobotClient= MyRobotClient(self.client,self.idx,self.currentRobotDescription)
				await myRobotClient.initialize()
				robotGet=await myRobotClient.readRobot()
				"""
				import time
				variabluesToUpdate =self.myRobotClient.currentRobotDescription.moveRobot( timestamp,enabled,Vlongi,Vrot)
				await self.myRobotClient.writeRobot(variabluesToUpdate)#force the update of only variables usefulls
				
				#robotGet=await self.myRobotClient.readRobot()
				
	async def setPosition(self,ts,mapId,poses):
		"""method to check connection and then send to server"""
		if self.client  is None :
			print ("e::::::::::::::client is None::::::::::::::,reconnect")
			print("setPosition::connect")
			self.connect()
			
		if self.client is not None :
			async with self.client:
				"""self.myRobotClient= MyRobotClient(self.client,self.idx,self.currentRobotDescription)
				await myRobotClient.initialize()
				robotGet=await myRobotClient.readRobot()
				"""
				import time
				#simple call to update a value
				#variabluesToUpdate =robotGet.setPosition(time.time(),-1,[11.0,12.0,13.0,0.0,0.0,1.5])#ts, mapid, txyz rxyz
				variabluesToUpdate =self.myRobotClient.currentRobotDescription.setPosition(ts,mapId,poses)#ts, mapid, txyz rxyz
				await self.myRobotClient.writeRobot(variabluesToUpdate)#force the update of only variables usefulls
				
				#robotGet=await self.myRobotClient.readRobot()
				
	async def readRobot(self):
		"""method to get all values from a robot"""
		async with self.client:
			self.currentRobotDescription= await self.myRobotClient.readRobot()