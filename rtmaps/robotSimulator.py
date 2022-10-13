#This is a template code. Please save it in a proper .py file.
import rtmaps.types
import numpy as np
import rtmaps.core as rt 
import rtmaps.reading_policy 
from rtmaps.base_component import BaseComponent # base class 

import asyncio
import logging
import sys
import os

#sys.path.insert(0, "..")

#pip install utm
import utm
import math




# Python class that will be called from RTMaps.
class rtmaps_python(BaseComponent):
	def __init__(self):
		BaseComponent.__init__(self) # call base class constructor

	def Dynamic(self):
		self.add_input("inputOdometryWanted", rtmaps.types.ANY) # define input
		self.add_output("ouputPosition", rtmaps.types.AUTO)
		
		
		self.add_property("defaultLatitude",49.383224), 
		self.add_property("defaultLongitude",1.072758)
		self.add_property("defaultYawDeg",0.0)
		

	def Birth(self):
		print("Python Birth")
		self._timeStamp = -1
		
		self.defaultLatitude=self.properties["defaultLatitude"].data
		self.defaultLongitude=self.properties["defaultLongitude"].data
		self.defaultYawDeg=self.properties["defaultYawDeg"].data
		
		#(utmx,utmy, tileid, tileLetter) =utm.from_latlon(self.defaultLatitude,self.defaultLongitude)
		self.pose=[self.defaultLatitude, self.defaultLongitude, 0.0,0.0,0.0,np.radians(self.defaultYawDeg)]

# Core() is called every time you have a new input
	def Core(self):
		
		timeStamp=rt.current_time()
		try :
			dataRead = self.inputs["inputOdometryWanted"].ioelt.data
		except:
			dataRead=None
			pass
		
		if dataRead is not None:
			#send new pose only if need
			if timeStamp != self._timeStamp:
				if self._timeStamp != -1:
					#get deltaTime
					deltaTimeS=(timeStamp-self._timeStamp)/1000000.0
					(utmx,utmy, tileid, tileLetter) =utm.from_latlon(self.pose[0] ,self.pose[1])
					yaw=math.pi/2.0-self.pose[5]

					if (dataRead[0]>0.0):
						deltaAngle=dataRead[2]*deltaTimeS
						deltaDist=dataRead[1]*deltaTimeS
					else:
						deltaAngle=0.0
						deltaDist=0.0
					
					utmx=utmx + deltaDist*math.cos( yaw+deltaAngle/2.0 ) 
					utmy=utmy + deltaDist*math.sin( yaw+deltaAngle/2.0 ) 
					newYaw=yaw+deltaAngle
					
					lati,longi=utm.to_latlon(utmx,utmy,tileid,tileLetter)
					
					self.pose = [lati,longi,0.0,0.0,0.0,math.pi/2.0-newYaw]
					
					#send pose
					currentPose = rtmaps.types.Ioelt()
					currentPose.data=[0.0,self.pose[0],self.pose[1],self.pose[2],self.pose[3],self.pose[4],self.pose[5]]
					currentPose.vector_size = len(currentPose.data)
					currentPose.ts = timeStamp
					self.outputs["ouputPosition"].write(currentPose)
					
				self._timeStamp=timeStamp
				
			
			
			
			
		

# Death() will be called once at diagram execution shutdown
	def Death(self):
		pass
