import asyncio
import sys

import logging
sys.path.insert(0, "..")
from asyncua import Server
from asyncua import ua
from asyncua.crypto.permission_rules import SimpleRoleRuleset
from asyncua.server.users import UserRole
from asyncua.server.user_managers import CertificateUserManager

logging.basicConfig(level=logging.INFO)

ENCRYPT=True


		
	

class MyRobot():
	def __init__(self,server,idx,robotName):
	
		self.server =server
		self.robotName =robotName
		self.idx=idx
		
		"""async with self.server:
			await self.server.nodes.objects.add_object(idx, robotName)
			self.pose = await myobj.add_variable(0, "pose", 0.0)
			self.poseVal=0.0
			await self.pose.set_writable()
		"""
		pass
		
	async def initialize(self):
	
		#async with self.server:
		self.currentobj =  await self.server.nodes.objects.add_object(self.idx, self.robotName)
		
		#rajout de variables
		self.ts_map_id_posexyzrxryrz= await self.currentobj.add_variable(self.idx, "ts_map_id_posexyzrxryrz", [0.0, -1.0,1000.0, 1000.0,1000.0,1000.0,1000.0,1000.0])
		await self.ts_map_id_posexyzrxryrz.set_writable() 
		
		self.ts_stdvposexyzrxryrz= await self.currentobj.add_variable(self.idx, "ts_map_id_posexyzrxryrz", [0.0, 1000.0, 1000.0,1000.0,1000.0,1000.0,1000.0])
		await self.ts_stdvposexyzrxryrz.set_writable() 
		
		self.robotStatusVal=0.0
		self.robotStatus = await self.currentobj.add_variable(self.idx, "robotStatus", self.robotStatusVal)
		await self.robotStatus.set_writable() 
		
		
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
		self.server =server
		
		#add entry points
		self.robotList=[]
		self.robotList.append(MyRobot(server,idx,"Jean-Michel(Segway)"))
		self.robotList.append(MyRobot(server,idx,"Jacqueline(AMI)"))
		self.robotList.append(MyRobot(server,idx,"Jean-Jacques(ESPACE)"))
		
		pass
		
	async def initialize(self):
		for robots in self.robotList:
				await robots.initialize()
		
	async def doGesture(self):
		for robot in self.robotList:
			await robot.doGesture()
		

async def main():

	cert_user_manager = CertificateUserManager()
	#await cert_user_manager.add_user("certificates/peer-certificate-example-1.der", name='test_user')
	#await cert_user_manager.add_user("vincent/my_cert.der", name='test_user')
	#await cert_user_manager.add_user("vincent/my_cert.der", name='VAUCHEY')
	#look her to know how to configure it
	await cert_user_manager.add_admin("vincent/my_cert.der", name='VAUCHEY')
	

	
	if ENCRYPT:
		server = Server(user_manager=cert_user_manager)
	else:
		server = Server()

	await server.init()

	server.set_endpoint("opc.tcp://127.0.0.1:4840/freeopcua/server/")
	if ENCRYPT:
		server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt],permission_ruleset=SimpleRoleRuleset())
	
		# load server certificate and private key. This enables endpoints
		# with signing and encryption.

		#await server.load_certificate("certificate-example.der")
		#await server.load_private_key("private-key-example.pem")
		
		#await server.load_certificate("vincent/my_cert.der")
		#await server.load_private_key("vincent/my_private_key.pem")
		
		await server.load_certificate("vincent/my_cert.der")
		await server.load_private_key("vincent/my_private_key.pem")
		
	#idx = 0
	uri = "http://esigelec.ddns.net"
	idx = await server.register_namespace(uri)
	
	print ("idx="+str(idx))
	# populating our address space
	myobj = await server.nodes.objects.add_object(idx, "MyObject")
	myvar = await myobj.add_variable(idx, "MyVariable", 0.0)
	myvarA = await myobj.add_variable(idx, "MyVariableA", 0.0)
	myvarC = await myobj.add_variable(idx, "MyVariableC", [6.7, 7.9])
	
	await myvarA.set_writable() 
	await myvarC.set_writable() 
	await myvar.set_writable()  # Set MyVariable to be writable by clients
	
	myobj2 = await server.nodes.objects.add_object(idx, "MyObject2")
	myvar2 = await myobj2.add_variable(idx, "MyVariable2", 2.0)
	await myvar2.set_writable()  # Set MyVariable to be writable by clients

	
	# starting!
	robotsGesture = RobotsGesture(server,idx)
	await robotsGesture.initialize()
	
	async with server:
		while True:
			await asyncio.sleep(1)
			current_val = await myvar.get_value()
			await robotsGesture.doGesture()#call the robot gesture 
			count = current_val + 0.1
			await myvar.write_value(count)
			await myvarA.write_value(-count)


if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	asyncio.run(main())
