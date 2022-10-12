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
	def __init__(self,server,robotName):
	
		self.server =server
		
		"""async with self.server:
			await self.server.nodes.objects.add_object(idx, robotName)
			self.pose = await myobj.add_variable(0, "pose", 0.0)
			self.poseVal=0.0
			await self.pose.set_writable()
		"""
		pass
		
	def doGesture(self):
	
		#ecriture de la nouvelle pose
		self.poseVal+=1.0
		"""async with self.server:
			await self.pose.write_value(self.poseVal)
		"""	
		pass
		
class RobotsGesture():
	def __init__(self,server):
		self.server =server
		
		#add entry points
		self.robotList=[]
		self.robotList.append(MyRobot(server,"Segway"))
		
		pass
		
	def doGesture(self):
		for robot in self.robotList:
			robot.doGesture()
		pass

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
	await myvar.set_writable()  # Set MyVariable to be writable by clients
	
	myobj2 = await server.nodes.objects.add_object(idx, "MyObject2")
	myvar2 = await myobj2.add_variable(idx, "MyVariable2", 2.0)
	await myvar2.set_writable()  # Set MyVariable to be writable by clients

	# starting!
	#robotsGesture =RobotsGesture(server)

	async with server:
		while True:
			await asyncio.sleep(1)
			current_val = await myvar.get_value()
			#await robotsGesture.doGesture()#call the robot gesture 
			count = current_val + 0.1
			await myvar.write_value(count)
			await myvarA.write_value(-count)


if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	asyncio.run(main())
