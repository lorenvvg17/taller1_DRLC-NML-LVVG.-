#!/usr/bin/python
import rospy
import serial, time
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class Node ():
   	def __init__(self):
        	self.rospy = rospy
        	self.rospy.init_node("nodo_control1", anonymous = True)
        	self.initParameters()
        	self.initPublishers()
        	self.main()

    	def initParameters(self):        
        	self.topic_lin = "/linear"
        	self.topic_ang = "/angular"
		self.serial = "/serial"
        	self.arduino = serial.Serial('/dev/ttyACM0', 9600)
        	self.msg_lin = String()
        	self.msg_ang = String()
        	self.V_lin = String()
        	self.V_ang = String()                     
        	return
   
    	def initPublishers(self):
       	 	self.pub_lin = self.rospy.Publisher(self.topic_lin, String, queue_size = 10)
        	self.pub_ang = self.rospy.Publisher(self.topic_ang, String, queue_size = 10)
        	return

    	def main (self):
        	print ("nodo OK")
        	while not self.rospy.is_shutdown():

        		
        		rawString = self.arduino.readline()
             		self.msg_lin,self.msg_ang = rawString.split(",")
             		self.V_lin = str(self.msg_lin)
			self.V_ang = str(self.msg_ang)
			self.pub_lin.publish(self.V_lin)
			self.pub_ang.publish(self.V_ang)
			print(self.V_lin,self.V_ang)

if __name__=="__main__":
    try:
        print("Iniciando Nodo")
        object = Node ()
    except rospy.ROSInterruptException:
        print ("Finalizando Nodo")
        pass
