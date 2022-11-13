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



UDP_PORT_BEGIN=5000
#ROBOT_ALLOWED_LIST=["Jean-Michel(Segway)","Jacqueline(AMI)","Jean-Jacques(ESPACE)","Fab1(MIR)"]
ROBOT_ALLOWED_LIST=["Jean-Michel(Segway)","Jacqueline(AMI)","Jean-Jacques(ESPACE)","Fab1(MIR)"]
#ROBOT_ALLOWED_LIST=["Jean-Michel(Segway)"]



UDP_IP = "127.0.0.1"

ENCRYPT=False
url = "opc.tcp://127.0.0.1:4840/freeopcua/server/"
#url = "opc.tcp://192.168.2.105:4840/freeopcua/server/"
namespace = "http://esigelec.ddns.net"#namespace
certificate="D:/data/apresBackup/COLIBRY/opcuaRT/opcuaRt/client/vincent/my_cert.der"#f"vincent/my_cert.der"
private_key="D:/data/apresBackup/COLIBRY/opcuaRT/opcuaRt/client/vincent/my_private_key.pem"#f"vincent/my_private_key.pem"

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("asyncua")

listOfName = listNames()
listofCLient=[]
i=0
for robotsNames  in ROBOT_ALLOWED_LIST :
	print ("create client for "+str(robotsNames)+" to udp port :"+str(UDP_PORT_BEGIN+i))
	#only create some robots
	currentRobotDescription = getCurrentRobotName(robotsNames)
	clientGesture = ClientGesture(url,namespace,certificate,private_key,ENCRYPT,currentRobotDescription)
	clientGesture.createSubprocessAndRunIt(1.0,robotsNames,UDP_PORT_BEGIN+i,False)
	
	listofCLient.append(clientGesture)
	
	i+=1
	
print ("number of process runned"+str(i))
while True:
	time.sleep(1)
	