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

async def browse_nodes(node: Node):
    """
    Build a nested node tree dict by recursion (filtered by OPC UA objects and variables).
    """
    node_class = await node.read_node_class()
    children = []
    for child in await node.get_children():
        if await child.read_node_class() in [ua.NodeClass.Object, ua.NodeClass.Variable]:
            children.append(
                await browse_nodes(child)
            )
    if node_class != ua.NodeClass.Variable:
        var_type = None
    else:
        try:
            var_type = (await node.read_data_type_as_variant_type()).value
        except ua.UaError:
            _logger.warning('Node Variable Type could not be determined for %r', node)
            var_type = None
    return {
        'id': node.nodeid.to_string(),
        'name': (await node.read_display_name()).Text,
        'cls': node_class.value,
        'children': children,
        'type': var_type,
    }
	
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
		uri = "http://esigelec.ddns.net"
		idx = await client.get_namespace_index(uri)
		print ("idx="+str(idx))
		#child = await objects.get_child([str(idx)+':MyObject', str(idx)+':MyVariable'])
		child = await objects.get_child([str(idx)+':MyObject', str(idx)+':MyVariable'])
		childA = await objects.get_child([str(idx)+':MyObject', str(idx)+':MyVariableA'])
		
		print(await child.get_value())
		print(await childA.get_value())
		await child.set_value(42.0)
		await childA.set_value(-42.0)
		print(await child.get_value())
		print(await childA.get_value())
		
		print ("try child 2")
		print ("dir(objects)="+str(dir(objects)))
		print ("objects.nodeid="+str(objects.nodeid))
		
		
		root = client.nodes.root
		_logger.info("Objects node is: %r", root)
		
		

		# Node objects have methods to read and write node attributes as well as browse or populate address space
		_logger.info("Children of root are: %r", await root.get_children())
		
		
		#print ("get_variables ="+str(root.get_variables()))
		#print ("get_children_description ="+str(root.get_children_description()))
		
		
		children = []
		for child in await root.get_children():
			print ("child="+str(child))
		
		#print (children)
			
		"""node=client.nodes.objects
		node_class = await node.read_node_class()
		children = []
		print ("get child")
		children = []
		chidlId=0
		for child in await node.get_children():
			if await child.read_node_class() in [ua.NodeClass.Object, ua.NodeClass.Variable]:
				if chidlId <10:
					children.append(
						await browse_nodes(child)
					)
				childId+=1
				
		print ("childreens="+str(children))
		
		#tree = await browse_nodes(client.nodes.objects)
		#_logger.info('Node tree: %r', tree)
		await client.disconnect()
		#browse_recursive(root)
		"""
		
		
		
		objects2 = client.nodes.objects
		child2 = await objects2.get_child([str(idx)+':MyObject2', str(idx)+':MyVariable2'])
		#child2 = await objects2.get_child([str(87)+':MyObject2', str(87)+':MyVariable2'])
		print(await child2.get_value())
		await child2.set_value(43.0)
		print(await child2.get_value())
		print(await child2.get_value())
		
		print ("finish")


def main():
	loop = asyncio.get_event_loop()
	loop.set_debug(True)
	loop.run_until_complete(task(loop))
	loop.close()


if __name__ == "__main__":
	main()
