import asyncio
import logging
import sys
sys.path.insert(0, "..")
from robotDescription import *

from ServerClient import *

from asyncua import Client, Node, ua
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256

CURRENT_ROBOT_NAME="Jean-Michel(Segway)"
currentRobotDescription = getCurrentRobotName(CURRENT_ROBOT_NAME)#recuperations des informations attends dans le robot current
assert (currentRobotDescription!=None, "robot not find")#verification que le robot existe

#################### CONFIG AREA START ####################
ENCRYPT=False#enable encryption

#url where to connecte
url = "opc.tcp://127.0.0.1:4840/freeopcua/server/"

namespace = "http://esigelec.ddns.net"#namespace

#USER certificate and key
#cert = f"certificates/peer-certificate-example-1.der"
#private_key = f"certificates/peer-private-key-example-1.pem"
cert=f"vincent/my_cert.der"
private_key=f"vincent/my_private_key.pem"


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
		print ("idx="+str(idx))
		
		myRobotClient= MyRobotClient(client,idx,currentRobotDescription)
		await myRobotClient.initialize()
		robotGet=await myRobotClient.readRobot()
		
		import time
		#simple call to update a value
		variabluesToUpdate =robotGet.setPosition(time.time(),-1,[11.0,12.0,13.0,0.0,0.0,1.5])#ts, mapid, txyz rxyz
		await myRobotClient.writeRobot(variabluesToUpdate)#force the update of only variables usefulls
		
		robotGet=await myRobotClient.readRobot()
		
		await client.disconnect()
		print ("finish")


def main():
	loop = asyncio.get_event_loop()
	loop.set_debug(True)
	loop.run_until_complete(task(loop))
	loop.close()


if __name__ == "__main__":
	main()
