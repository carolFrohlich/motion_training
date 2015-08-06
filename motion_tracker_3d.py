import socket
import struct

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
import math
from objloader import *
import os

import sys


coord_scale= 0.1
rotation_scale = 20


###### start psychopy ######
#creates a full screen window and draw a white cross on the screen while waiting for inputs
############################
pygame.init()

screen_info = pygame.display.Info()
#display = (800,600)
display = (screen_info.current_w, screen_info.current_h)


pichu = pygame.image.load(os.path.join('assets', 'pichu.png'))
pichurect = pichu.get_rect()
pichurect.centerx = display[0] / 2 - display[0] * 0.2
pichurect.centery += display[0] * 0.2
plane = pygame.image.load(os.path.join('assets', 'plane.png'))
planerect = plane.get_rect()
planerect.centerx = display[0] / 2 
planerect.centery += display[0] * 0.2
brain = pygame.image.load(os.path.join('assets', 'brain2.png'))
brainrect = brain.get_rect()
brainrect.centerx = display[0] / 2 + display[0] * 0.2
brainrect.centery += display[0] * 0.2



screen = pygame.display.set_mode(display, DOUBLEBUF|RESIZABLE)

#user choose obj
screen.blit(pichu, pichurect)
screen.blit(plane, planerect)
screen.blit(brain, brainrect)
pygame.display.flip()

option = 0
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN and event.key == pygame.K_1:
			option = 1
		elif event.type == KEYDOWN and event.key == pygame.K_2:
			option = 2
		elif event.type == KEYDOWN and event.key == pygame.K_3:
			option = 3

	if option != 0:
		break


pichu = None
plane = None
brain = None
screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL|RESIZABLE)
glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, 1);

zoom = -200
#if brain
if option == 3:
	glLightfv(GL_LIGHT0, GL_POSITION,  (0, -400, 200, 2.5))
	glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
	glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1.0))
	#glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1.0))
	#glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)


else:
	glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
	glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
	glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1.0))
	glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1.0))
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)

	glLightfv(GL_LIGHT1, GL_POSITION,  (-40, -200, 100, 0.0))
	glLightfv(GL_LIGHT1, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
	glLightfv(GL_LIGHT1, GL_DIFFUSE, (1, 1, 1, 1.0))
	glEnable(GL_LIGHT1)

	glLightfv(GL_LIGHT2, GL_POSITION,  (40, 200, 100, 0.0))
	glLightfv(GL_LIGHT2, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
	glLightfv(GL_LIGHT2, GL_DIFFUSE, (1, 1, 1, 1.0))
	glEnable(GL_LIGHT2)

	glLightfv(GL_LIGHT3, GL_POSITION,  (40, -200, 100, 0.0))
	glLightfv(GL_LIGHT3, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
	glLightfv(GL_LIGHT3, GL_DIFFUSE, (1, 1, 1, 1.0))
	glEnable(GL_LIGHT3)


glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded


glMatrixMode( GL_PROJECTION )
glLoadIdentity()
gluPerspective(45, (display[0]/display[1]), 0.1, 800.0)



#if pichu
if option == 1:
	zoom = -1
	brain = OBJ('pichu/pichu13.obj', swapyz=True)
	glTranslatef(0.0,0.0, zoom)


# #if plane
elif option == 2:
	zoom = -400
	brain = OBJ('plane.obj', swapyz=True)
	glTranslatef(0.0,0.0, zoom)
	glRotatef(90.0, 0.0, 1.0, 0.0)
	glRotatef(-90.0, 1.0, 0.0, 0.0)


#if brain
else:
	zoom = -500
	glMaterialfv(GL_FRONT, GL_SPECULAR,  (1.0, 1.0, 1.0, 50.0))
	glMaterialfv(GL_FRONT, GL_SHININESS, (50.0))
	glColor([1.0,0.4,0.6])
	brain = OBJ('gm.obj', swapyz=True)

	glTranslatef(0.0,0.0, zoom)
	#glRotatef(90.0, 1.0, 0.0, 0.0)
	#glRotatef(180.0, 0.0, 1.0, 0.0)




glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

glCallList(brain.gl_list)
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
		#print params
		#scale coordinates.
		#coords = [element*coord_scale for element in params]

		scale = np.abs(zoom * coord_scale)

		coords = []
		coords.append(params[0]*scale)
		coords.append(params[1]*scale)
		coords.append(params[2]*scale)
		coords.append(params[3])#/2*math.pi)*360)
		coords.append(params[4])#/2*math.pi)*360)
		coords.append(params[5])#/2*math.pi)*360)


		#and don't let the cross leave the screen
		# coords = [0.8 if element> 0.8 else element for element in coords]
		# coords = [-0.8 if element< -0.8 else element for element in coords]
		

		###### set cross color according to movment ######
		# calculates distance between last frame head position and current head position.
		# If participant is almost not moving (distance is <0.1) set color to green
		# if movment is between 0.1 and 0.1, set color to yelow.
		# and if participant is moving too much (distance >= 0.2) set color to red
		mov_distance = np.linalg.norm(np.asarray(params) - np.asarray(old_params))

		# glClearColor(0, 0.6, 0, 0.0)
		# if mov_distance >= 0.2:
		# 	glClearColor(1, 0.5, 0.5, 0.0)
		# elif mov_distance < 0.2 and mov_distance > 0.1:
		# 	glClearColor(0.6, 0.6, 0, 0.0)
		
		#update screen

		glMatrixMode( GL_MODELVIEW )
		glLoadIdentity()


		#glTranslatef(coords[1], coords[0], coords[2])
		#glRotatef(rotation_scale, coords[4], coords[3], coords[5])
		print coords[4], coords[3], coords[5]
		glRotatef(coords[4]*rotation_scale, 1.0, 0.0, 0.0)
		glRotatef(coords[3]*rotation_scale, 0.0, 1.0, 0.0)
		glRotatef(coords[5]*rotation_scale, 0.0, 0.0, 1.0)


		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		glCallList(brain.gl_list)

		#keep the current paramenter for calculation distance in the next TR
		old_params = params

		pygame.display.flip()