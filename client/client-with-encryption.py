import asyncio
import logging
import sys
import time
import os
import socket
#sys.path.insert(0, "..")
#sys.path.append( os.path.abspath(sys.path[0]+"/../"))
sys.path.insert(0, os.path.abspath(sys.path[0]+"/../"))
from robotDescription import *

from ClientGesture import *

from asyncua import Client, Node, ua
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256


import subprocess

#CURRENT_ROBOT_NAME="Jean-Michel(Segway)"
CURRENT_ROBOT_NAME="Fab1(MIR)"
print ("robots availaibles :"+str(listNames()))

currentRobotDescription = getCurrentRobotName(CURRENT_ROBOT_NAME)#recuperations des informations attends dans le robot current
assert (currentRobotDescription!=None)#verification que le robot existe

#################### CONFIG AREA START ####################
ENCRYPT=False#enable encryption

#url where to connecte
url = "opc.tcp://127.0.0.1:4840/freeopcua/server/"
#url = "opc.tcp://192.168.2.105:4840/freeopcua/server/"

namespace = "http://esigelec.ddns.net"#namespace

#USER certificate and key
#cert = f"certificates/peer-certificate-example-1.der"
#private_key = f"certificates/peer-private-key-example-1.pem"
cert="D:/data/apresBackup/COLIBRY/opcuaRT/opcuaRt/client/vincent/my_cert.der"#f"vincent/my_cert.der"
private_key="D:/data/apresBackup/COLIBRY/opcuaRT/opcuaRt/client/vincent/my_private_key.pem"#f"vincent/my_private_key.pem"


#################### CONFIG AREA END ####################

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("asyncua")



			
async def task(loop):
	
	#url = "opc.tcp://admin@127.0.0.1:4840/freeopcua/server/"
	client = Client(url=url)
	#client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") 
	if ENCRYPT:
		await client.set_security(
			SecurityPolicyBasic256Sha256,
			certificate=cert,
			private_key=private_key,
			#server_certificate="certificate-example.der"
			server_certificate=cert #"vincent/my_cert.der"server_certificate="vincent/my_cert.der"
			#mode=ua.MessageSecurityMode.SignAndEncrypt
		)
		#mode=ua.MessageSecurityMode.SignAndEncrypt
	
	async with client:
		#objects = client.nodes.objects
		
		idx = await client.get_namespace_index(namespace)
		print ("!!!!! idx="+str(idx))
		
		myRobotClient= MyRobotClient(client,idx,currentRobotDescription)
		await myRobotClient.initialize()
		robotGet=await myRobotClient.readRobot()
		
		import time
		
		for i in range(100):
			print ("!!!!! send new position")
			#simple call to update a value
			variabluesToUpdate =robotGet.setPosition(time.time(),-1,[11.0+i*0.1,12.0,13.0,0.0,0.0,1.5])#ts, mapid, txyz rxyz
			await myRobotClient.writeRobot(variabluesToUpdate)#force the update of only variables usefulls
			
			robotGet=await myRobotClient.readRobot()
			print ("!!!!! robot ts_map_id_posexyzrxryrz:"+str( robotGet.currentRobotDescription.ts_map_id_posexyzrxryrz))

		await client.disconnect()
		print ("!!!!! finish")

"""
def main():
	loop = asyncio.get_event_loop()
	loop.set_debug(True)
	loop.run_until_complete(task(loop))
	loop.close()

https://docs.python.org/3/library/multiprocessing.html
"""

def task5():

	UDP_IP = "127.0.0.1"
	UDP_PORT=5006
	
	clientGesture = ClientGesture(url,namespace,cert,private_key,ENCRYPT,currentRobotDescription)
	
	
	clientGesture.createSubprocessAndRunIt(1.0,CURRENT_ROBOT_NAME,UDP_PORT,False)
	#while True:
	#	time.sleep(1.0)
	#	pass



	
	
	
	#command+="print (\"will create process\")" +"\n"
	#command+="clientGesture.createProcessAndRunIt(1.0)"+"\n"
	#command+="print (\"will create process done\")" +"\n"
	
	
	
	#sys.path.insert(0, "..")



	
	for i in range(2):
		print ("i="+str(i))
		time.sleep(1.0)
		
		
	clientGesture.setPosition(0.0,0.0,[1.0,2.0,3.0,4.0,5.0,6.0])

	time.sleep(1.0)
	clientGesture.readVariables()
	
	print ("clientGesture.ts_map_id_posexyzrxryrz="+str(clientGesture.ts_map_id_posexyzrxryrz))
	#print ("clientGesture.stdev_ts_map_id_posexyzrxryrz="+str(clientGesture.stdev_ts_map_id_posexyzrxryrz))
	#print ("clientGesture.ts_map_id_posexyzrxryrz_target="+str(clientGesture.ts_map_id_posexyzrxryrz_target))
	#print ("clientGesture.robotStatus="+str(clientGesture.robotStatus))
	print ("clientGesture.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec="+str(clientGesture.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec))
	#print ("clientGesture.robotName="+str(clientGesture.robotName))
	

	time.sleep(1.0)
	clientGesture.readVariables()
	
	print ("clientGesture.ts_map_id_posexyzrxryrz="+str(clientGesture.ts_map_id_posexyzrxryrz))
	#print ("clientGesture.stdev_ts_map_id_posexyzrxryrz="+str(clientGesture.stdev_ts_map_id_posexyzrxryrz))
	#print ("clientGesture.ts_map_id_posexyzrxryrz_target="+str(clientGesture.ts_map_id_posexyzrxryrz_target))
	#print ("clientGesture.robotStatus="+str(clientGesture.robotStatus))
	print ("clientGesture.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec="+str(clientGesture.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec))
	#print ("clientGesture.robotName="+str(clientGesture.robotName))
	
	
	for i in range(5):
		#print ("read:"+str(subp.stdout.read(10)))
		#print ("read:"+str(subp.stdout.readline()))
		time.sleep(1.0)
		
	#client part
	"""
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	serverAddressPort   = (UDP_IP, UDP_PORT)
	
	commandtoExecute="clientGesture.setPosition(0.0,0.0,[1.0,2.0,3.0,4.0,5.0,6.0])"
	sock.sendto(str.encode(commandtoExecute), serverAddressPort)
	print ("wait data")
	bytesAddressPair = sock.recvfrom(1024)
	message = bytesAddressPair[0]
	address = bytesAddressPair[1]
	print ("message2 ="+str(message))
	print ("address ="+str(address))
	
	
	commandtoExecute="clientGesture.moveRobot(0.0,1.0,2.0,time.time())"
	sock.sendto(str.encode(commandtoExecute), serverAddressPort)
	print ("wait data")
	bytesAddressPair = sock.recvfrom(1024)
	message = bytesAddressPair[0]
	address = bytesAddressPair[1]
	print ("message2 ="+str(message))
	print ("address ="+str(address))
	
	for i in range(5):
		#print ("read:"+str(subp.stdout.read(10)))
		#print ("read:"+str(subp.stdout.readline()))
		time.sleep(1.0)
	"""
	
	#print ("read:"+str(subp.stdout.read(10)))
	
def task4():
	"""test en mode multi process"""
	import time
	
	clientGesture = ClientGesture(url,namespace,cert,private_key,ENCRYPT,currentRobotDescription)

	print ("createProcessAndRunIt call")
	clientGesture.createProcessAndRunIt(1.0)
	print ("createProcessAndRunIt call done")
	
	
	
	for i in range(5):
		#clientGesture.pipOut2.send("salut"+str(i))
		#clientGesture.setPosition(0.0,0.0,[1.0+time.time(),2.0-time.time(),3.0,4.0,5.0,6.0])
		#time.sleep(1.0)
	
		print ("try to read variables")
		clientGesture.readVariables()
		try :
			print("()()()()clientGesture.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec="+str(clientGesture.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec))
			print("()()()()clientGesture.ts_map_id_posexyzrxryrz="+str(clientGesture.ts_map_id_posexyzrxryrz))
		except:
			pass
		time.sleep(1.0)
		"""
		clientGesture.waitVariables()
		dataReceived=clientGesture.pipOutM.recv()
		print ("!!!!!!!!!!!!!dataReceived="+str(dataReceived))
		exec(
		"""
	time.sleep(5)
	print ("will kill process")
	clientGesture.stopProcess()
	
def task3():
	"""test en mode multri thread"""
	import time
	
	clientGesture = ClientGesture(url,namespace,cert,private_key,ENCRYPT,currentRobotDescription)
	
	print ("creaThreadAndRunIt call")
	clientGesture.creaThreadAndRunIt(1.0)
	print ("creaThreadAndRunIt call done")
	
	print("wait ready")
	while not clientGesture.getIsReady():
		time.sleep(0.5)
	print("wait ready done")
	
	
	import time
	for i in range(10):
		print ("~~~~~~send position")
		clientGesture.setPosition(0.0,0.0,[1.0+time.time(),2.0-time.time(),3.0,4.0,5.0,6.0])
		print ("~~~~~~send position done")
		
		clientGesture.moveRobot(0.0,1.0,2.0,time.time())
		time.sleep(0.5)
		
		
		
async def task2():
	timeToTest=120.0
	
	
	clientGesture = ClientGesture(url,namespace,cert,private_key,ENCRYPT,currentRobotDescription)
	print ("!!!!!!!!!!!!!!!!!!!!!!will run a clientGesture.connect")
	await clientGesture.connect()#do a connectio (enable encryption)
	#print (dir(clientGesture.client))
	#assert(1==2)
	print ("!!!!!!!!!!!!!!!!!!!!!!will run clientGesture.getCurrentRobot")
	#await clientGesture.client.connect()
	#async with clientGesture.client :
	if True:
		await clientGesture.getCurrentRobot()
		print ("!!!!!!!!!!!!!!!!!!!!!!clientGesture.getCurrentRobot done")
		
		timeStart=time.time()
		while ((time.time()-timeStart) < timeToTest):
			#lecture du robot
			print ("!!!!!!!!!!!!!!!!!!!!!!will run clientGesture.readRobot")
			robotGet = await clientGesture.readRobot()
			if robotGet is not None:
				print ("!!!!!!!!!!!!!!!!!!!!!! robot ts_map_id_posexyzrxryrz:"+str( robotGet.ts_map_id_posexyzrxryrz))
			
			
			await clientGesture.moveRobot(0.0,1.0,2.0,3.0)
			
			print ("send position")
			await clientGesture.setPosition(0.0,0.0,[1.0+time.time(),2.0,3.0,4.0,5.0,6.0])
			
			#sleep a short while
			await asyncio.sleep(0.05)
		
		print ("!!!!!!!!!!!!!!!!!!!!!!finish")
		#await clientGesture.client.disconnect()
	
def main():
	#loop = asyncio.get_event_loop()
	#loop.set_debug(True)
	#loop.run_until_complete(task(loop))
	#loop.close()
	#asyncio.run(task2())
	#task3()#multi thread
	#task4()#multi process
	task5()#multi process
	
	
	
	#clientGesture = ClientGesture(url,namespace,cert,private_key,ENCRYPT,currentRobotDescription)
	#asyncio.run(task2A(clientGesture))
	#asyncio.run(task2B(clientGesture))
	
	#loop = asyncio.get_event_loop()
	#loop.set_debug(True)
	#loop.run_until_complete(task2())
	#loop.close()

"""

def main():
	clientGesture = ClientGesture(url,namespace,cert,private_key,ENCRYPT,currentRobotDescription)
	print ("!!will run a clientGesture.connect")
	asyncio.run(clientGesture.connect())#do a connection
	print ("!!will run a clientGesture.connect done")
	import time
	timeStamp=time.time()
	data=[1.0,2.0,3.0,4.0,5.0,6.0]
	asyncio.run(clientGesture.setPosition(timeStamp,-1,data))
"""

	
if __name__ == "__main__":
	main()
