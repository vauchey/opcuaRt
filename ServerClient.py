

from robotDescription import *

from asyncua import Client, Node, ua
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256

from asyncua import Server
from asyncua import ua
from asyncua.crypto.permission_rules import SimpleRoleRuleset
from asyncua.server.users import UserRole
from asyncua.server.user_managers import CertificateUserManager


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
		for values in  self.currentRobotDescription.__dict__.keys():
			if  values!="robotName":
				self.__dict__[values+"_child"] = await self.objects.get_child([str(self.idx)+':'+self.robotName, str(self.idx) + ':'+values])#recupere les childs (une fois pour toute)
		pass
		

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
			
			
#############server area

class MyRobotServer():
	
	def __init__(self,server,idx,robotDescription):
		""" class de creation d'un robot vote server"""
		self.server =server
		self.idx=idx
		self.robotDescription = robotDescription
		
		
		pass
		
	async def initialize(self):
		"""methode d'initialisation d'un robot cote serve"""		
		self.robotName =  await self.server.nodes.objects.add_object(self.idx, self.robotDescription.__dict__["robotName"])#add the robot name
		print ("self.robotDescription.robotName="+str(self.robotDescription.__dict__["robotName"]))
		for values in  self.robotDescription.__dict__.keys():
			if  values!="robotName":
				#rajout du robot Name
				self.__dict__[values]= await self.robotName.add_variable(self.idx,values,self.robotDescription.__dict__[values])
				await self.__dict__[values].set_writable() 
				print ("create "+str(values)+" "+str(self.robotDescription.__dict__[values]))
		print ("initialize start done")
		
		
		
		self.robotStatusVal=0.0
		
		pass
		
	async def doGesture(self):
		
		#ecriture de la nouvelle pose
		self.robotStatusVal+=1.0
		await self.robotStatus.write_value(self.robotStatusVal)
		"""async with self.server:
			await self.pose.write_value(self.poseVal)
		"""	
		pass
		
class RobotsGesture():
	
	def __init__(self,server,idx):
		""" class de gestion de plusieurs robots cote server"""
		self.server =server
		
		#add entry points
		ROBOT_LIST
		self.robotList=[]
		for robots in ROBOT_LIST:
			self.robotList.append(MyRobotServer(server,idx,robots))
		
		pass
		
	async def initialize(self):
		for robots in self.robotList:
				await robots.initialize()
		
	async def doGesture(self):
		for robot in self.robotList:
			await robot.doGesture()
		