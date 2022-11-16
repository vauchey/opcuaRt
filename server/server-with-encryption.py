import asyncio
import sys

import logging
sys.path.insert(0, "..")
from robotDescription import *
from ServerGesture import *



logging.basicConfig(level=logging.INFO)

#################### CONFIG AREA START ####################
ENCRYPT=True

#add your admin and user, only admin can write data
ADMIN_DICT={}
#ADMIN_DICT["VAUCHEY"] = {"certificate": "vincent/my_cert.der", "key":"vincent/my_private_key.pem" }
ADMIN_DICT["AMI"] = {"certificate": "../../generate/AMI/my_cert.der", "key":"../../generate/AMI/my_private_key.pem" }
ADMIN_DICT["ESPACE"] = {"certificate": "../../generate/ESPACE/my_cert.der", "key":"../../generate/ESPACE/my_private_key.pem" }
ADMIN_DICT["MIR1"] = {"certificate": "../../generate/MIR1/my_cert.der", "key":"../../generate/MIR1/my_private_key.pem" }
ADMIN_DICT["Segway"] = {"certificate": "../../generate/segway/my_cert.der", "key":"../../generate/segway/my_private_key.pem" }
USER_DICT={}


		

#url where to connecte
#url = "opc.tcp://127.0.0.1:4840/freeopcua/server/"
url = "opc.tcp://192.168.2.149:11111/freeopcua/server/"
#url = "opc.tcp://192.168.2.105:4840/freeopcua/server/"

namespace = "http://esigelec.ddns.net"#namespace

#################### CONFIG AREA START ####################
	


async def main():

	cert_user_manager = CertificateUserManager()
	#await cert_user_manager.add_user("certificates/peer-certificate-example-1.der", name='test_user')
	#await cert_user_manager.add_user("vincent/my_cert.der", name='test_user')
	#await cert_user_manager.add_user("vincent/my_cert.der", name='VAUCHEY')
	#look her to know how to configure it
	#await cert_user_manager.add_admin("vincent/my_cert.der", name='VAUCHEY')
	if ENCRYPT:
		for admins in ADMIN_DICT.keys():
			await cert_user_manager.add_admin(ADMIN_DICT[admins]["certificate"], name=admins)
			
		#user cannot write data
		for users in USER_DICT.keys():
			await cert_user_manager.add_admin(USER_DICT[users]["certificate"], name=users)
	
	
	if ENCRYPT:
		server = Server(user_manager=cert_user_manager)
	else:
		server = Server()

	await server.init()

	server.set_endpoint(url)#"opc.tcp://127.0.0.1:4840/freeopcua/server/"
	if ENCRYPT:
		server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt],permission_ruleset=SimpleRoleRuleset())
	
		# load server certificate and private key. This enables endpoints
		# with signing and encryption.
		for admins in ADMIN_DICT.keys():
			await server.load_certificate(ADMIN_DICT[admins]["certificate"])
			await server.load_private_key(ADMIN_DICT[admins]["key"])
			
		for users in USER_DICT.keys():
			await server.load_certificate(USER_DICT[users]["certificate"])
			await server.load_private_key(USER_DICT[users]["key"])
			
		
		#await server.load_certificate("vincent/my_cert.der")
		#await server.load_private_key("vincent/my_private_key.pem")
		
	#idx = 0
	
	idx = await server.register_namespace(namespace)
	
	print ("idx="+str(idx))
	# populating our address space
	
	# starting!
	robotsGesture = RobotsGesture(server,idx)
	await robotsGesture.initialize()
	
	async with server:
		while True:
			await asyncio.sleep(0.01)
			#current_val = await myvar.get_value()
			await robotsGesture.doGesture()#call the robot gesture 
			#count = current_val + 0.1
			#await myvar.write_value(count)
			#await myvarA.write_value(-count)


if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	asyncio.run(main())
