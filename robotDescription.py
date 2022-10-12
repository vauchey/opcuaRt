
class ROBOT_GENERIC():
	def __init__(self):
		self.ts_map_id_posexyzrxryrz = [0.0, -1.0,1000.0, 1000.0,1000.0,1000.0,1000.0,1000.0]
		self.ts_map_id_posexyzrxryrz = [0.0, 1000.0, 1000.0,1000.0,1000.0,1000.0,1000.0]
		self.robotStatus=0.0 

class ROBOT_WITH_WHEEL(ROBOT_GENERIC):
	def __init__(self,robotName):
		super().__init__()
		self.robotName="robotName"
		
		pass
		
		
		
robotList=[]
robotList.append(ROBOT_WITH_WHEEL("Jean-Michel(Segway)"))
robotList.append(ROBOT_WITH_WHEEL("Jacqueline(AMI)"))
robotList.append(ROBOT_WITH_WHEEL("Jean-Jacques(ESPACE)"))
