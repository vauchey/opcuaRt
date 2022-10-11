import asyncio
import logging
import sys
sys.path.insert(0, "..")
from asyncua import Client, Node, ua
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256

ENCRYPT=True

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("asyncua")

cert_idx = 1
#cert = f"certificates/peer-certificate-example-{cert_idx}.der"
#private_key = f"certificates/peer-private-key-example-{cert_idx}.pem"
cert=f"vincent/my_cert.der"
private_key=f"vincent/my_private_key.pem"


async def task(loop):
	url = "opc.tcp://127.0.0.1:4840/freeopcua/server/"
	#url = "opc.tcp://admin@127.0.0.1:4840/freeopcua/server/"
	client = Client(url=url)
	#client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") 
	if ENCRYPT:
		await client.set_security(
			SecurityPolicyBasic256Sha256,
			certificate=cert,
			private_key=private_key,
			#server_certificate="certificate-example.der"
			server_certificate="vincent/my_cert.der"
			#mode=ua.MessageSecurityMode.SignAndEncrypt
		)
		#mode=ua.MessageSecurityMode.SignAndEncrypt
	
	async with client:
		objects = client.nodes.objects
		child = await objects.get_child(['0:MyObject', '0:MyVariable'])
		print(await child.get_value())
		await child.set_value(42.0)
		print(await child.get_value())
		print(await child.get_value())
		print ("finish")


def main():
	loop = asyncio.get_event_loop()
	loop.set_debug(True)
	loop.run_until_complete(task(loop))
	loop.close()


if __name__ == "__main__":
	main()
