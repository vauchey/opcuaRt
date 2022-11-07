

from robotDescription import *

import logging
from asyncua import Client, Node, ua
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256
from requests.exceptions import ConnectionError
import threading
import time
import asyncio


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
				
		print ("MyRobotClient::readRobot"+str(self.currentRobotDescription.__dict__))
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
			
			
def check_connection(func):
	"""decorator to detect error ,remove client and force reconnect"""
	async def  wrapper(*args, **kwargs):
		#args[0] is the self of the class
		print ("args="+str(args))
		#print ("kwargs="+str(**kwargs))
		try:
		
			if args[0].client is None:
				print("try ::connect")
				await args[0].connect()
				
				await args[0].getCurrentRobot()
			return await func(*args, **kwargs)
			#return func(*args,**kwargs)
			#except ua.utils.SocketClosedException:
			#except ConnectionError
			#except ua.utils.UaError:
		except Exception as e:
			args[0].client=None
			args[0].logger.info("Error:"+str(e))
			print ("!!!!!!!!!!!!!! check_connection detect an error!!!!!!!!!!!!!!!!!")
			#raise (e)
	return(wrapper)
		
def do_writing(func):
	async def wrapper2(*args, **kwargs):
		#variabluesToUpdate =self.myRobotClient.currentRobotDescription.setPosition(ts,mapId,poses)#ts, mapid, txyz rxyz
		#await self.myRobotClient.writeRobot(variabluesToUpdate)#force the update of only variables usefulls
		print (" call variabluesToUpdate =self.myRobotClient.currentRobotDescription."+str(func.__name__)+"(*args, **kwargs)")
		#eval("variabluesToUpdate=args[0].myRobotClient.currentRobotDescription."+str(func.__name__)+"(*args, **kwargs)")
		#variabluesToUpdate=eval("args[0].myRobotClient.currentRobotDescription."+str(func.__name__)+"(*args, **kwargs)")
		print ("args="+str(args))
		#variabluesToUpdate=args[0].myRobotClient.currentRobotDescription.setPosition(args[1],args[2],args[3])
		variabluesToUpdate=eval("args[0].myRobotClient.currentRobotDescription."+str(func.__name__)+"("+ ",".join( "args["+str(i)+"]" for i in range(1,len(args)))  +")")
		print (" variabluesToUpdate="+str(variabluesToUpdate))
		return await args[0].myRobotClient.writeRobot(variabluesToUpdate)
		
	return(wrapper2)

def automatically_call_fromDescription(func):
	"""decorateur to automatically call fonction from robotDescritpion and then ask the loop to update the properties needed"""
	def wrapper3(*args, **kwargs):
		args[0].lock.acquire()
		try :
			msgToEval="args[0].myRobotClient.currentRobotDescription."+str(func.__name__)+"("+ ",".join( "args["+str(i)+"]" for i in range(1,len(args)))  +")"
			print ("call "+str(msgToEval))
			variabluesToUpdate=eval(msgToEval)
			for variables in variabluesToUpdate:
				if variables not in args[0].listOfValueToSend :
					args[0].listOfValueToSend.append(variables)
		finally:
			args[0].lock.release()
		pass
		
	return(wrapper3)
	
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
		self.logger = logging.getLogger("asyncua")
		self.socketTimout=1.0
		
		self.isReady=False
		self.robotHasChanged=False
		
	def creaThreadAndRunIt(self,periodInS):
		self.listOfValueToSend=[]
		self.lock = threading.Lock()
		self.currentThread=threading.Thread(target=self.runProcessTask, args=[periodInS] )
		self.currentThread.start()
		
	def runProcessTask(self,periodInS):
		#while True:
		#	print ("runProcessTask working")
		#	time.sleep(0.5)
		asyncio.run(self.processTask(periodInS))
		
	def getIsReady(self):
		self.lock.acquire()
		isReady=self.isReady
		self.lock.release()
		return isReady
		
	async def processTask(self,periodInS):
		""" thread asyncio permetant de communiquer avec le server"""
		
		#clientGesture = ClientGesture(self.url,self.namespace,self.certificate,self.private_key,self.ENCRYPT,self.currentRobotDescription)
		#await clientGesture.connect()
		await self.connect()# force une premiere connection
		
		await self.getCurrentRobot()#force de recuperer le robot courrant
		
		self.lock.acquire()
		self.isReady=True
		self.lock.release()
		
		self.timeStart=time.time()
		while not self.isDying():
		
			################ change robot if needed
			self.lock.acquire()
			robotHasChanged=self.robotHasChanged
			self.robotHasChanged=False
			self.lock.release()
			if robotHasChanged:
				await self.getCurrentRobot()#force de recuperer le robot courrant, car celui selectione a change
				self.robotHasChanged
			
			################ send variable which need to be send			
			self.lock.acquire()
			try :
				#update all variales to server
				await self.updateVariables(self.listOfValueToSend)
			finally:
				self.lock.release()
			
			################ read robot
			robotGet = await self.readRobot()
			if robotGet is not None:
				print ("!!!!!!!!!!!!!!!!!!!!!! robot ts_map_id_posexyzrxryrz:"+str( robotGet.ts_map_id_posexyzrxryrz))
				
				#on appelle les callbacks de sortie
				self.sendRobotInformations(robotGet)
				
			await asyncio.sleep(periodInS)#on fait une petite pause
			
			
		#await clientGesture.client.disconnect() #ne marche pas vraiment


	
	
	async def connect(self):
		"""method to connect to server"""
		self.client = Client(url=self.url, timeout =self.socketTimout)
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
			
		await self.client.connect()#fait une vraie connection
		
		
	


	@check_connection
	async def updateVariables(self, variablesToUpdate):
		if len(self.listOfValueToSend)> 0:
			print ("updates variables :"+str(self.listOfValueToSend))
			await self.myRobotClient.writeRobot(variablesToUpdate)#force the update of only variables usefulls
			print ("updates variables done:"+str(self.listOfValueToSend))
			self.listOfValueToSend=[]


	@check_connection
	async def getCurrentRobot(self):
		"""permet de seconnecter au bon robot, peut etre appeller depuis lexterieur en cas de changement de robot"""
		self.idx = await self.client.get_namespace_index(self.namespace)
		self.myRobotClient= MyRobotClient(self.client,self.idx,self.currentRobotDescription)
		await self.myRobotClient.initialize()
		#except ua.utils.SocketClosedException:
		#	self.logger.info("Socket has closed connection")
		#		self.client= None

	
				
	
	@check_connection
	async def readRobot(self):
		"""method to get all values from a robot, it is a method which is not decorated becore we read the entire robot values"""

		self.currentRobotDescription= await self.myRobotClient.readRobot()
		return self.currentRobotDescription
		
	#liste des methodes denvoi au server decorées avec (do_writing)
	
	

	
		
				

	"""
	@check_connection
	@do_writing
	async def setPosition(self,ts,mapId,poses):
		#method to check connection and then send to server
		pass
	"""
	def changeRobot(self, currentRobotDescription):
		print ("call setPosition")
		self.lock.acquire()
		try :
			self.myRobotClient.currentRobotDescription=currentRobotDescription
			self.robotHasChanged=True
		finally:
			self.lock.release()
		pass
		
		
	#############metdhode to redefine for ros or rtmaps
	def sendRobotInformations(self,robotGet):
		"""function to redefine for ros or rtmaps, for example on rtmaps it will be start writing, and on ros a publisher"""
		print ("sendRobotInformations :: wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec ="+str(robotGet.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec))
		print ("sendRobotInformations :: ts_map_id_posexyzrxryrz ="+str(robotGet.ts_map_id_posexyzrxryrz))
		print ("sendRobotInformations :: wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec ="+str(robotGet.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec))
		
		
	def isDying(self):
		"""function to redefine for ros or rtmaps, for example on rtmaps it will be rt.is_dying()"""
		
		if (time.time()-self.timeStart) > 10.0:
			return True
		else:
			return False
			
	#############metdhode to have access from ros or rtmaps
	@automatically_call_fromDescription
	def setPosition(self,ts,mapId,poses):
		pass
		
	@automatically_call_fromDescription
	def moveRobot(self, timestamp,enabled,Vlongi,Vrot):
		"""method to check connection and then send to server a movement"""
		pass
		
		
	@automatically_call_fromDescription
	def moveToPose(self,timestamp, mapId, poseXYZrXYZ):
		"""ask to go to a pose"""
		pass
		
		
		
		
		
		
		
		"""
		print ("call setPosition")
		self.lock.acquire()
		try :
			print ("will ask to send positions :"+str(poses))
			variabluesToUpdate =self.myRobotClient.currentRobotDescription.setPosition(ts,mapId,poses)#ts, mapid, txyz rx
			#met a jour la liste des variables a updater
			for variables in variabluesToUpdate:
				if variables not in self.listOfValueToSend :
					self.listOfValueToSend.append(variables)
		finally:
			self.lock.release()
		"""
		

		
	"""
	async def setPosition(self,ts,mapId,poses):
		variabluesToUpdate =self.myRobotClient.currentRobotDescription.setPosition(ts,mapId,poses)#ts, mapid, txyz rxyz
		await self.myRobotClient.writeRobot(variabluesToUpdate)#force the update of only variables usefulls
	"""