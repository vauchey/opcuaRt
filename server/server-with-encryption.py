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
		
	idx = 0

	# populating our address space
	myobj = await server.nodes.objects.add_object(idx, "MyObject")
	myvar = await myobj.add_variable(idx, "MyVariable", 0.0)
	await myvar.set_writable()  # Set MyVariable to be writable by clients

	# starting!

	async with server:
		while True:
			await asyncio.sleep(1)
			current_val = await myvar.get_value()
			count = current_val + 0.1
			await myvar.write_value(count)


if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	asyncio.run(main())
