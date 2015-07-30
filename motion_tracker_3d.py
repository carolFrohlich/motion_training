import socket
import struct

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
from objloader2 import *

import sys


coord_scale=10.0



###### start psychopy ######
#creates a full screen window and draw a white cross on the screen while waiting for inputs
############################
pygame.init()
display = (800,600)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, 1)
#glLightfv(GL_LIGHT0, GL_POSITION,  (0.0, 0.0, 800.0, 50.0))
glLightfv(GL_LIGHT0, GL_POSITION,  (0.0, 0.0, 800.0, 50.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 0.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 0.0))
glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 0.0))

glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)

glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 0.0) )
glMaterialfv(GL_FRONT, GL_SHININESS,(50.0))


glMatrixMode( GL_PROJECTION )
glLoadIdentity()
gluPerspective(45, (display[0]/display[1]), 0.1, 500.0)
glTranslatef(0.0,0.0, -200)
glRotatef(90.0,45.0,0.0, 0.0)


glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
brain = OBJ('XY_Pichu.obj', swapyz=True)
#brain2 = OBJ('rh.pial.obj', swapyz=True)
glCallList(brain.gl_list)
#glCallList(brain2.gl_list)
pygame.display.flip()
print('finish loading')


###### start socket ######
# Listens the port in which afni rt will send the movement parameters.
# The default values for running afni rt locally are: ip=127.0.0.1 and port=53214
# for running on the server: ip=0.0.0.0 and port=8000
############################
TCP_IP = '127.0.0.1'
TCP_PORT = 53214
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()


old_params = [0.0]*6

###### now things are actually happening ######
# enters in the while loop when the sender is ready.
# parses the movement paramenters and update the screen accordingly
# exit when not receiving more data
############################
while 1:

	data = conn.recv(BUFFER_SIZE)

	# finish the script when sender don't have more data to send
	if not data: break

	# receive 6 mov params in binary. 
	# The data len is 24, so each parameter has len 4.  
	# we parse them and put in vector params.
	# Because not all data we receive movement paramenters, 
	# we check if data actually has movement params. 
	if len(data) == 24:
		params = []
		for i in range(6):
			param = struct.unpack('f',  data[i*4:i*4+4])[0]
			params.append(param)

		###### update screen ######

		#scale coordinates.
		coords = [element*coord_scale for element in params]


		#and don't let the cross leave the screen
		# coords = [0.8 if element> 0.8 else element for element in coords]
		# coords = [-0.8 if element< -0.8 else element for element in coords]
		

		###### set cross color according to movment ######
		# calculates distance between last frame head position and current head position.
		# If participant is almost not moving (distance is <0.1) set color to green
		# if movment is between 0.1 and 0.1, set color to yelow.
		# and if participant is moving too much (distance >= 0.2) set color to red
		mov_distance = np.linalg.norm(np.asarray(params) - np.asarray(old_params))

		color = [0.0, 1.0, 0.0]
		if mov_distance >= 0.2:
			color = [1.0, 0.0, 0.0]
		elif mov_distance < 0.2 and mov_distance > 0.1:
			color = [1.0, 1.0, 0.0] 
		

		#update screen

		glMatrixMode( GL_MODELVIEW )
		glLoadIdentity()
		
		#glColor(color)
		glMaterialfv(GL_FRONT, GL_DIFFUSE, color )
		glMaterialfv(GL_FRONT, GL_AMBIENT, color )

		glTranslatef(coords[0], coords[2], coords[1])
		glRotatef(coord_scale, coords[3], coords[5], coords[4])
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		glCallList(brain.gl_list)
		#glCallList(brain2.gl_list)

		#keep the current paramenter for calculation distance in the next TR
		old_params = params

		pygame.display.flip()