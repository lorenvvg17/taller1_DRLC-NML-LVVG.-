#!/usr/bin/python
import rospy
import serial, time
#from std_msgs.msg import Integer
from std_msgs.msg import String, Float64
from geometry_msgs.msg import Twist

class Node ():
   	def __init__(self):
        	self.rospy = rospy
        	self.rospy.init_node("nodo_control1", anonymous = True)
        	self.initParameters()
        	self.initPublishers()
        	self.main()

    	def initParameters(self):        
        	self.topic_lin = "/lineal"
        	self.topic_ang = "/angular"
		self.serial = "/serial"
        	self.arduino = serial.Serial('/dev/ttyACM0', 9600)
        	self.msg_lin = String()
        	self.msg_ang = String()
        	                     
        	return
   
    	def initPublishers(self):
       	 	self.pub_lin = self.rospy.Publisher(self.topic_lin, String, queue_size = 10)
        	self.pub_ang = self.rospy.Publisher(self.topic_ang, String, queue_size = 10)
        	return

    	def main (self):
        	print ("nodo OK")
        	while not self.rospy.is_shutdown():
			
        		#self.rate.sleep()
        		rawString = self.arduino.readline()
             		self.msg_lin.data,self.msg_ang.data = rawString.split(",")
             		
			self.pub_lin.publish(self.msg_lin)
			self.pub_ang.publish(self.msg_ang)
			print(self.msg_lin,self.msg_ang)

if __name__=="__main__":
    try:
        print("Iniciando Nodo")
        object = Node ()
    except rospy.ROSInterruptException:
        print ("Finalizando Nodo")
        pass
