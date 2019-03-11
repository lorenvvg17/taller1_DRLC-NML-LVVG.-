#!/usr/bin/python

import rospy
import math

from std_msgs.msg import Bool
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class Node ():
    def __init__(self):
        self.rospy = rospy
        self.rospy.init_node("nodo_control2", anonymous = True)
        self.initParameters()
        self.initSubscribers()
        self.initPublishers()

        self.main()

    def initParameters(self):
        #VARIABLES DEL NODO
	self.ranges = "/scan.ranges"
        self.topic_aux = "/aux_topic"
        self.topic_laser = "/scan"
        self.msg_laser = LaserScan()

        self.msg_aux = Bool()
        self.change_laser = False
        self.rate = self.rospy.Rate(50)

        return

    def callback_laser(self, msg):
        #conversion de radianes a grados de angulo minimo y de incremento
	self.angulos = []
	self.angulo_incremento = (180*msg.angle_increment)/math.pi
	self.angulos.append((180*(msg.angle_min))/math.pi)
        #creacion de lista de rangos
	self.rangos = msg.ranges
	self.rangos=list(self.rangos)


	#print (self.angulos)


	self.size_vector = len(self.rangos)

	#lectura = msg.ranges[360]
        #print (self.pepito)
        #contruccion de vector de angulos de lectura
	for i in range (0,self.size_vector-1):
		self.angulofor=(self.angulos[i]+self.angulo_incremento)
		self.angulos.append(self.angulofor)

        #tranformacion de inf a un numero grande para evitar que lo tenga en cuenta
	self.inf = float ('inf')
	self.newrangos = []
	for (i,item) in enumerate(self.rangos):
		if item == self.inf:
			item = 80
		self.newrangos.append(item)
		self.rangos = self.newrangos

        #PASO DE COORDENADAS POLARES A RECTANGULARES
	self.cartesianasx= []
	self.cartesianasy= []
	for j in range (0, self.size_vector):
		self.sin=math.sin(self.angulos[j])
		self.cos=math.cos(self.angulos[j])
		self.carx= self.rangos[j]*self.sin
		self.cary= self.rangos[j]*self.cos
		if self.cary>0 and self.cary<2:
			self.cartesianasx.append(self.carx)
			self.cartesianasy.append(self.cary)

			self.cartesianasx.append(0)
			self.cartesianasy.append(0)

            #DELIMITACION DE RANGO DE LECTURA

	for k in range (len(self.cartesianasy)):
		if self.cartesianasy[k] <= 2 and self.cartesianasy[k]>=0:
			self.cartesianasy[k]=self.cartesianasy[k]
		else:
			self.cartesianasy[k]=0
	#print(self.cartesianasy)

        #CREACION DE VECTOR DE DISTANCIAS
	self.size = len(self.cartesianasy)
	self.distancia= []
	for k in range (0, self.size-1):
		if self.size <= k+1:
			break;
		else:
			self.resty = (self.cartesianasy[k+1]-self.cartesianasy[k])**2
			self.restx = (self.cartesianasx[k+1]-self.cartesianasx[k])**2
			self.sumxy = self.restx + self.resty
			self.sqrt = math.sqrt(self.sumxy)
			self.distancia.append(self.sqrt)

	#print (list(self.distancia))



    #AGRUPACION DE PUNTOS

	self.G_P = []
	self.num1 = float ('1')
	self.num0 = float ('0')
	for x in range (len(self.distancia)):
   		if self.distancia [x] < 1:
			self.distancia[x] = 1
		else:
			self.distancia[x] = 0

	self.contador= 0;

    #DISTANCIA ENTRE PUNTOS
	for x in range (0, len(self.distancia)):
		if len(self.distancia) == x+1:
			break;
		else:
			if self.distancia[x]==1 and self.distancia[x+1]==1:
				self.contador= self.contador+1

			else:
				self.G_P.append(self.contador)
				self.contador=0


	for x in range (0,len(self.G_P)):
		if len(self.G_P) == x:
			break;
		else:
			if self.G_P[x]>10:

				print ('(obstaculo)')




	print('.')

    	self.change_laser = True
    	return

    def initSubscribers(self):
        #SUSCRIPTORES???
        self.sub_laser = self.rospy.Subscriber(self.topic_laser, LaserScan, self.callback_laser)
        return

    def initPublishers(self):
        #PUBLICADORES
        self.pub_aux = self.rospy.Publisher(self.topic_aux, Bool, queue_size = 10)
        return


    def main (self):
        #CODIGO PRINCIPAL
        print ("nodo OK")




        while not self.rospy.is_shutdown():
            if self.change_laser:
                self.rate.sleep()
            #    self.msg_aux.topic.x = float(self.msg_laser)
            #    self.pub_aux.publish (self.msg_aux)
            #    self.change_laser = False



if __name__=="__main__":
    try:
        print("Iniciando Nodo")
        object = Node()
    except rospy.ROSInterruptException:
        print ("Finalizando Nodo")
        pass
