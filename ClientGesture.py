

from robotDescription import *

import logging
from asyncua import Client, Node, ua
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256
from requests.exceptions import ConnectionError
import threading
import multiprocessing
import time
import asyncio
import sys
import socket 
import subprocess

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
		#print ("args="+str(args))
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
		#print (" call variabluesToUpdate =self.myRobotClient.currentRobotDescription."+str(func.__name__)+"(*args, **kwargs)")
		#eval("variabluesToUpdate=args[0].myRobotClient.currentRobotDescription."+str(func.__name__)+"(*args, **kwargs)")
		#variabluesToUpdate=eval("args[0].myRobotClient.currentRobotDescription."+str(func.__name__)+"(*args, **kwargs)")
		#print ("args="+str(args))
		#variabluesToUpdate=args[0].myRobotClient.currentRobotDescription.setPosition(args[1],args[2],args[3])
		variabluesToUpdate=eval("args[0].myRobotClient.currentRobotDescription."+str(func.__name__)+"("+ ",".join( "args["+str(i)+"]" for i in range(1,len(args)))  +")")
		print (" variabluesToUpdate="+str(variabluesToUpdate))
		return await args[0].myRobotClient.writeRobot(variabluesToUpdate)
		
	return(wrapper2)

def automatically_call_fromDescription(func):
	"""decorateur to automatically call fonction from robotDescritpion and then ask the loop to update the properties needed"""
	def wrapper3(*args, **kwargs):
		if args[0].sock is not None:
			print ("call un runInSubProcess with sock")

			commandtoExecute="clientGesture."+str(func.__name__)+"("+ ",".join( str(args[i]) for i in range(1,len(args)))  +")"
			print ("rrrrrrrrrrrrrrr: commandtoExecute="+str(commandtoExecute))
			args[0].sock.sendto(str.encode(commandtoExecute), args[0].serverAddressPort)
			print ("wait data")
			bytesAddressPair = args[0].sock.recvfrom(1024)
			message = bytesAddressPair[0]
			address = bytesAddressPair[1]
			print ("message2 ="+str(message))
			print ("address ="+str(address))
			#print ("args[0].robotGet = "+str(args[0].robotGet))
			#print ("args[0].robotGet = "+str(args[0].robotGet.__dir__))
			
		elif args[0].runInMultriProcess == True:
			print ("call un runInMultriProcess == True")
			#envoit dans le pipe-in-python un message qui sera directement evalue
			#msgToEval="object."+str(func.__name__)+"("+ ",".join( "args["+str(i)+"]" for i in range(1,len(args)))  +")"
			msgToEval="object."+str(func.__name__)+"("+ ",".join( "["+str(args[i])+"]" for i in range(1,len(args)))  +")"
			print ("in multiprocess, call "+str(msgToEval))
			args[0].pipOutM.send(msgToEval)
		else:
			print ("call un runInMultriProcess == False")
			#cas ou en multi thread uniquement
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
		self.neewReadDone=False
		self.runInMultriProcess=False
		
		self.sock = None
		self.subp=None
		
		
	def __del__(self):
		if self.subp is not None :
			self.subp.kill()
			self.subp=None
			
	def createSubprocessAndRunIt(self,periodInS,CURRENT_ROBOT_NAME,UDP_PORT,disableSubProcess):
		UDP_IP = "127.0.0.1"
		command=""
	
		command+="import asyncio"+"\n"
		command+="import logging"+"\n"
		command+="import time"+"\n"
		command+="import sys"+"\n"
		command+="import socket"+"\n"
		command+="UDP_IP = \"127.0.0.1\""+"\n"
		command+="UDP_PORT = "+str(UDP_PORT)+"\n"
		command+="sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)"+"\n"
		command+="sock.bind((UDP_IP, UDP_PORT))"+"\n"
		
		#sys.path.insert(0, "..")

		command+="sys.path.insert(0, \""+str(sys.path[0].replace("\\","/"))+"\")"+"\n"
		
		command+="from robotDescription import *"+"\n"
		command+="from ClientGesture import *"+"\n"
		
		command+="CURRENT_ROBOT_NAME=\""+str(CURRENT_ROBOT_NAME)+"\""+"\n"
		command+="currentRobotDescription = getCurrentRobotName(CURRENT_ROBOT_NAME)"+"\n"
		
		command+="clientGesture = ClientGesture(\""+str(self.url)+"\",\""+str(self.namespace)+"\" , \""+str(self.certificate)+"\" , \""+str(self.private_key)+"\" ,"+str(self.ENCRYPT)+",currentRobotDescription)"+"\n"
		
		

		#command+="clientGesture.listOfValueToSend=[]" +"\n"
		#command+="clientGesture.lock = threading.Lock()" +"\n"	
		#command+="asyncio.run(clientGesture.processTask(1.0))" +"\n"
		
		
		command+="print (\"creaThreadAndRunIt call\")" +"\n"
		command+="clientGesture.creaThreadAndRunIt(0.1)" +"\n"
		command+="print (\"creaThreadAndRunIt call done\")" +"\n"
		
		command+="while not clientGesture.getIsReady():" +"\n"
		command+="\ttime.sleep(0.5)" +"\n"
			
		command+="while True:"+"\n"

		command+="\tbytesAddressPair = sock.recvfrom(1024)" +"\n"
		command+="\tmessage = bytesAddressPair[0]" +"\n"
		command+="\ttry:" +"\n"
		command+="\t\treturnMsg=eval(message.decode())" +"\n"
		command+="\texcept:" +"\n"
		command+="\t\treturnMsg=None" +"\n"
		
		command+="\taddress = bytesAddressPair[1]" +"\n"
		#command+="\tsock.sendto(str.encode(\"salut3\"), address)" +"\n"
		command+="\tsock.sendto(str.encode(str(returnMsg)), address)" +"\n"
		print ("command="+str(command))
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.serverAddressPort   = (UDP_IP, UDP_PORT)

	
		
		if not disableSubProcess:
			self.subp = subprocess.Popen(["C:\\ProgramData\\Anaconda3\\python.exe", "-c", command], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)#
			
			#self.subp = subprocess.Popen(["C:\\ProgramData\\Anaconda3\\python.exe", "-c", command],shell=False)
		#print ("read:"+str(subp.stdout.read(10)))
		
	def creaThreadAndRunIt(self,periodInS):
		"""fonction pour creer un thread et le lancer"""
		print(" creaThreadAndRunIt called")
		self.listOfValueToSend=[]
		self.lock = threading.Lock()
		self.currentThread=threading.Thread(target=self.runProcessTask, args=[periodInS] )
		self.currentThread.start()
		print(" creaThreadAndRunIt called done")
		
	def createProcessAndRunIt(self,periodInS):
		"""fonction pour creer un process, le lancer et il lancera la partie thread"""
		#pour s'inspirer https://superfastpython.com/multiprocessing-pipe-in-python/
		print(" createProcessAndRunIt called")
		self.listOfValueToSend=[]
		#self.lock = threading.Lock()
		self.pipOutM, self.pipOutS=multiprocessing.Pipe(duplex=True)
		self.runInMultriProcess=True 
		self.currentProcess = multiprocessing.Process(target=self.runMultiProcessTask, args=[periodInS,self.pipOutS] )
		self.currentProcess.start()
		
	def stopProcess(self):
		self.currentProcess.terminate()
		
	def readVariables(self):
		"""function to read variables from multiprocessing """
		if self.sock is not None :
			commandtoExecute="clientGesture.robotGet.__dict__"
			self.sock.sendto(str.encode(commandtoExecute), self.serverAddressPort)
			
			print ("wait data")
			bytesAddressPair = self.sock.recvfrom(1024)
			message = bytesAddressPair[0]
			address = bytesAddressPair[1]
			print ("message3 ="+str(message))
			print ("address ="+str(address))
			try:
				currentDict= eval(message)
				if ( currentDict is not None) and ( type(currentDict) == type({})):
					self.__dict__.update(currentDict)
					return True
				return False
			except:
				print ("!!cannot update current dict")
				return False
				
			
		
		else :
			if self.pipOutM.poll(0.1):
				dataReceived=self.pipOutM.recv()
				print ("!!!!!!!!!!!!!dataReceived="+str(dataReceived))
				commandToExecute=dataReceived.split("\n")
				for commands in commandToExecute:
					print ("    execute :"+str(commands))
					exec(commands)
				#exec(dataReceived)
				return True
			else:
				print ("!!!!!!!!!!!!!no data")
				return False
	
	def runMultiProcessTask(object, period,pipOut):
		""" sous processus qui lance le thread et execute les methodes"""
		#create the lock and run the thread
		object.pipOutS=pipOut
		object.runInMultriProcess=False 
		print ("period="+str(period))
		object.creaThreadAndRunIt(period)
		
		while True:
			readValue=object.pipOutS.recv()
			print ("readValue="+str(readValue))
			eval(readValue)#execution de la fonction
		
			
		#object.pipOut.send("salut")
		#while 1:
			
		
		"""object.listOfValueToSend=[]
		object.lock = threading.Lock()
	
		print("runMultiProcessTask called")
		print("object"+str(object))
		print("period"+str(period))
		
		object.runProcessTask(period)
		"""
		
		
	def runProcessTask(self,periodInS):
		print (" runProcessTask call with period = "+str(periodInS))
		#while True:
		#	print ("runProcessTask working")
		#	#time.sleep(0.5)
		print (" runProcessTask call")
		asyncio.run(self.processTask(periodInS))
		
		"""
		#loop = asyncio.get_event_loop()
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		print ("will call run_coroutine_threadsafe")
		future = asyncio.run_coroutine_threadsafe(self.processTask(periodInS), loop)
		print ("will call future.result")
		# Wait for the result:
		result = future.result()
		print ("   runProcessTask call done")
		"""
	def getIsReady(self):
		self.lock.acquire()
		isReady=self.isReady
		self.lock.release()
		return isReady
		
	async def processTask(self,periodInS):
		""" thread asyncio permetant de communiquer avec le server"""
		print ("calllllllllllllllll processTask with period"+str(periodInS))
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
			
			
			############### function to get command (mainly usefull for rtmaps side)
			self.getCommand()

			################ send variable which need to be send			
			self.lock.acquire()
			try :
				#update all variales to server
				await self.updateVariables(self.listOfValueToSend)
			finally:
				self.lock.release()
			
			################ read robot
			self.lock.acquire()
			try:
				self.robotGet = await self.readRobot()
			finally:
				self.lock.release()
				
			if self.robotGet is not None:
				print ("self.robotGet = "+str(self.robotGet.__dict__))
				pass#print ("!!!!!!!!!!!!!!!!!!!!!! robot ts_map_id_posexyzrxryrz:"+str( robotGet.ts_map_id_posexyzrxryrz))
				
				
				#on appelle les callbacks de sortie
				self.sendRobotInformations(self.robotGet)
				
			await self.mysleep(periodInS)
			#await asyncio.sleep(periodInS)
			
			
		#await clientGesture.client.disconnect() #ne marche pas vraiment

	async def mysleep(self,periodInS):
		await asyncio.sleep(periodInS)#on fait une petite pause
	
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
		print ("call changeRobot")
		self.lock.acquire()
		try :
			self.myRobotClient.currentRobotDescription=currentRobotDescription
			self.robotHasChanged=True
		finally:
			self.lock.release()
		pass
		
		
	#############metdhode to redefine for ros or rtmaps
	def getCommand(self):
		pass
		
	def sendRobotInformations(self,robotGet):
		"""function to redefine for ros or rtmaps, for example on rtmaps it will be start writing, and on ros a publisher"""
		print ("sendRobotInformations :: wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec ="+str(robotGet.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec))
		print ("sendRobotInformations :: ts_map_id_posexyzrxryrz ="+str(robotGet.ts_map_id_posexyzrxryrz))
		print ("sendRobotInformations :: wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec ="+str(robotGet.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec))
		
		#check if multiprocess pipe
		hasPiOutS=False
		try :
			self.pipOutS
			hasPiOutS=True
		except :
			pass
		
		if hasPiOutS:
			msg=""
			msg+="self.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec="+str(robotGet.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec)
			msg+="\n"
			msg+="self.ts_map_id_posexyzrxryrz="+str(robotGet.ts_map_id_posexyzrxryrz)
			self.pipOutS.send(msg)
			#self.pipOutS.send("self.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec="+str(robotGet.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec))
			#self.pipOutS.send("self.ts_map_id_posexyzrxryrz="+str(robotGet.ts_map_id_posexyzrxryrz))
		#self.pipOut.send("robotGet.ts_map_id_posexyzrxryrz="+str(robotGet.ts_map_id_posexyzrxryrz))
		
	def isDying(self):
		"""function to redefine for ros or rtmaps, for example on rtmaps it will be rt.is_dying()"""
		if (time.time()-self.timeStart) > 30.0:
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