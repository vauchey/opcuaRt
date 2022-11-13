
class ROBOT_GENERIC():
	def __init__(self):
		""" attention, toutes les valeurs definies en tant que self seront transmises via opc ua"""
		self.ts_map_id_posexyzrxryrz = [0.0, -1.0,1000.0, 1000.0,1000.0,1000.0,1000.0,1000.0]#pose in meters
		self.stdev_ts_map_id_posexyzrxryrz = [0.0, 1000.0, 1000.0,1000.0,1000.0,1000.0,1000.0]
		
		self.ts_map_id_posexyzrxryrz_target = [0.0, -1.0,1000.0, 1000.0,1000.0,1000.0,1000.0,1000.0]#target
		
		self.robotStatus=0.0 #enumt do describe the status
		self.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec=[0.0,0.0,0.0,0.0]

	def setPosition(self,timestamp, mapId, poseXYZrXYZ):
		"""methode to sendback robot pose,re turn the variables wich needs to be updated to the server
		poseXYZrXYZ is meter and rad
		
		"""
		assert( len(poseXYZrXYZ) ==6,"poseXYZrXYZ size muse be 6")
		self.ts_map_id_posexyzrxryrz[0]=float(timestamp)
		self.ts_map_id_posexyzrxryrz[1]=float(mapId)
		self.ts_map_id_posexyzrxryrz[2:]=poseXYZrXYZ
		
		return ["ts_map_id_posexyzrxryrz"]#do not forger to send back list of variables to update

	def moveToPose(self,timestamp, mapId, poseXYZrXYZ):
		"""high level function to ask a robot to move to a specified position, the robot need to have the abailibility to do pat planning, control and obstacle detection"""
		assert( len(poseXYZrXYZ) ==6,"poseXYZrXYZ size muse be 6")
		self.ts_map_id_posexyzrxryrz_target[0]=timestamp
		self.ts_map_id_posexyzrxryrz_target[1]=mapId
		self.ts_map_id_posexyzrxryrz_target[2:]=poseXYZrXYZ
		
		return ["ts_map_id_posexyzrxryrz_target"]#do not forger to send back list of variables to update
		

	
	def moveRobot(self, timestamp,enabled,Vlongi,Vrot):
		""" ask the robot to move with specified Vlongi (m/s) and Vrot (rad/s)"""
		self.wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec=[float(timestamp),float(enabled),float(Vlongi),float(Vrot)]
		return ["wantedSpeed_Ts_enable_Vlongimbysec_Vrotradbysec"]
		
	
		
class ROBOT_WITH_WHEEL(ROBOT_GENERIC):
	def __init__(self,robotName):
		super().__init__()
		self.robotName=robotName #this variable is needed to create a node
		
		pass
		
		
		
		
ROBOT_LIST=[]
ROBOT_LIST.append(ROBOT_WITH_WHEEL("Jean-Michel(Segway)"))
ROBOT_LIST.append(ROBOT_WITH_WHEEL("Jacqueline(AMI)"))
ROBOT_LIST.append(ROBOT_WITH_WHEEL("Jean-Jacques(ESPACE)"))
ROBOT_LIST.append(ROBOT_WITH_WHEEL("Fab1(MIR)"))

def getCurrentRobotName(name):
	for robots in ROBOT_LIST:
		if robots.robotName == name:
			return robots
	return None
	
def getCurrentRobotNameIndex(name):
	i=0
	for robots in ROBOT_LIST:
		if robots.robotName == name:
			return i
		i+=1
	return -1

def listNames():
	robotNameList=[]
	for robots in ROBOT_LIST:
		robotNameList.append(robots.robotName)
	return robotNameList