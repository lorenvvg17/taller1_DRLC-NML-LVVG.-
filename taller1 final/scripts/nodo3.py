#!/usr/bin/python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist


class Node ():
    def __init__(self):
        self.rospy = rospy
        self.rospy.init_node("nodo_control3", anonymous = True)
        self.initParameters()
        self.initSubscribers()
        self.initPublishers()
        self.main()

    def initParameters(self):
        	self.topic_lin = "/lineal"
        	self.topic_ang = "/angular"
        	self.topic_aux = "/aux_topic"
        	self.topic_vel = "/cmd_vel"
		self.V_lin = String()
		self.V_ang = String()
		self.msg_aux = Bool()
    		self.msg_vel = Twist()
        	self.change_V_lin = False
        	self.change_V_ang = False
        	self.change_aux = False
        	self.rate = self.rospy.Rate(50)
        	return

    def callback_pot1(self, msg):
        	self.V_lin = msg.data
        	self.change_V_lin = True
        	return

    def callback_pot2(self, msg):
        	self.V_ang = msg.data
        	self.change_V_ang = True
        	return

    def callback_aux(self, msg):
        	self.msg_aux = msg.data
        	self.change_aux = True
        	return

    def initSubscribers(self):
        
        	self.sub_lin = self.rospy.Subscriber(self.topic_lin, String, self.callback_pot1)
        	self.sub_ang = self.rospy.Subscriber(self.topic_ang, String, self.callback_pot2)
        	self.sub_aux = self.rospy.Subscriber(self.topic_aux, Bool, self.callback_aux)
       		return

    def initPublishers(self):
        
       		self.pub_vel = self.rospy.Publisher(self.topic_vel, Twist, queue_size = 10)
        	return


    def main (self):
        #CODIGO PRINCIPAL
	print ("nodo OK")
        
        while not self.rospy.is_shutdown():
            if self.change_V_ang and self.change_V_lin and self.change_aux:
                    if self.msg_aux == True:
                        self.msg_vel.linear.x= 0
                        self.msg_vel.angular.z=float(self.V_ang)
                        self.pub_vel.publish(self.msg_vel)
			
                    else:
                        self.msg_vel.linear.x = float(self.V_lin)
                        self.msg_vel.angular.z = float(self.V_ang)
                        self.pub_vel.publish (self.msg_vel)
			self.change_V_ang = False
			self.change_V_lin = False
			self.change_aux = False
	
        return
	


if __name__=="__main__":
    try:
        print("Iniciando Nodo")
        object = Node ()
    except rospy.ROSInterruptException:
        print ("Finalizando Nodo")
        pass
