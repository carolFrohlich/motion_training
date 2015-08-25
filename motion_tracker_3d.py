import socket
import struct

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
import math
import objloader as loader
#import fasterobj as fasterloader
import os

import sys


coord_scale= 0.002
rotation_scale = 1.5


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



screen = pygame.display.set_mode(display, DOUBLEBUF|RESIZABLE|FULLSCREEN)

#user choose obj
screen.blit(pichu, pichurect)
screen.blit(plane, planerect)
screen.blit(brain, brainrect)
pygame.display.flip()

option = 0
while True:
	for event in pygame.event.get():
		if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
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

zoom = 0
#if brain
if option == 3:
	glLightfv(GL_LIGHT0, GL_POSITION,  (0, -400, 200, 2.5))
	glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
	glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1.0))
	#glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1.0))
	#glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)


else:
	glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 100, 100, 0.0))
	glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
	glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1.0))
	glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1.0))
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)

	glLightfv(GL_LIGHT1, GL_POSITION,  (-40, -100, 100, 0.0))
	glLightfv(GL_LIGHT1, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
	glLightfv(GL_LIGHT1, GL_DIFFUSE, (1, 1, 1, 1.0))
	glEnable(GL_LIGHT1)

	glLightfv(GL_LIGHT2, GL_POSITION,  (40, 100, 100, 0.0))
	glLightfv(GL_LIGHT2, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
	glLightfv(GL_LIGHT2, GL_DIFFUSE, (1, 1, 1, 1.0))
	glEnable(GL_LIGHT2)

	glLightfv(GL_LIGHT3, GL_POSITION,  (40, -100, 100, 0.0))
	glLightfv(GL_LIGHT3, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
	glLightfv(GL_LIGHT3, GL_DIFFUSE, (1, 1, 1, 1.0))
	glEnable(GL_LIGHT3)


glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded


glMatrixMode( GL_PROJECTION )
glLoadIdentity()
gluPerspective(45, 1.5, 0.01, 800.0)




#if pichu
if option == 1:
	pichu_happy = loader.OBJ('pichu/pichu_head2_happy.obj', swapyz=True)
	pichu_ok = loader.OBJ('pichu/pichu_head2_ok.obj', swapyz=True)
	pichu_sad = loader.OBJ('pichu/pichu_head2_sad.obj', swapyz=True)
	zoom = -0.55
	brain = pichu_happy
	body = loader.OBJ('pichu/pichu_body5.obj', swapyz=True)
	glTranslatef(0.0,0.0, zoom)
	coord_scale = 0.002


# #if plane
elif option == 2:
	zoom = -1
	brain = loader.OBJ('plane9.obj', swapyz=True)
	glTranslatef(0.0,0.0, zoom)
	coord_scale = 0.1


#if brain
else:
	zoom = -1
	glMaterialfv(GL_FRONT, GL_SPECULAR,  (1.0, 1.0, 1.0, 50.0))
	glMaterialfv(GL_FRONT, GL_SHININESS, (50.0))
	glColor([1.0,0.4,0.6])
	brain = loader.OBJ('brain18.obj', swapyz=True)

	glTranslatef(0.0,0.0, zoom)
	coord_scale  = 0.1



glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

glCallList(brain.gl_list)

if option == 1:
	glCallList(body.gl_list)
	
	



pygame.display.flip()
print('finish loading')


###### start socket ######
# Listens the port in which afni rt will send the movement parameters.
# The default values for running afni rt locally are: ip=127.0.0.1 and port=53214
# for running on the server: ip=0.0.0.0 and port=8000
############################
TCP_IP = '0.0.0.0'
TCP_PORT = 53214
CONTROL_SIZE = 8
BUFFER_SIZE = 1024
l_onoff=1
l_linger=0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_LINGER,struct.pack('ii',l_onoff,l_linger))

s.bind((TCP_IP, TCP_PORT))
s.listen(1)

print 'connecting'

conn, addr = s.accept()


old_params = [0.0]*6

###### now things are actually happening ######
# enters in the while loop when the sender is ready.
# parses the movement paramenters and update the screen accordingly
# exit when not receiving more data
############################
while 1:

	data = conn.recv(CONTROL_SIZE)

	# finish the script when sender don't have more data to send
	if not data or len(data) != 8: 
		print "recived bogus control message %s (%d)"%(data,len(data))
		continue

	print len(data)

	data_lengths=struct.unpack('ii',data)
	if data_lengths[0] == 0 and data_lengths[1] == 0:
    	# we have received a terminate request from the user
    	# respond
		conn.send(data)
		# then exit, the remote end will kill the connection
		break

	if data_lengths[0] != 0:
		# we have a bogus header, read and discard
		data = conn.recv(data_lengths[0])


	# receive 6 mov params in binary. 
	# The data len is 48, so each parameter has len 8 (double).  
	# we parse them and put in vector params.
	# Because not all data we receive movement paramenters, 
	# we check if data actually has movement params. 
	elif data_lengths[1] == 48:
		data = conn.recv(data_lengths[1])
		params=struct.unpack('dddddd',data)


		print params

		###### update screen ######

		coords = []
		coords.append(params[0]*coord_scale)
		coords.append(params[1]*coord_scale)
		coords.append(params[2]*coord_scale)
		coords.append(params[3]*rotation_scale)
		coords.append(params[4]*rotation_scale)
		coords.append(params[5]*rotation_scale)

		#and don't let the obj leave the screen
		for c in range(3):
			if coords[c] > 0.35:
				coords[c] = 0.35
			if coords[c] < -0.35:
				coords[c] = -0.35

		###### set background color according to movment ######
		# calculates distance between last frame head position and current head position.
		# If participant is almost not moving (distance is <0.1) set color to green
		# if movment is between 0.1 and 0.1, set color to yelow.
		# and if participant is moving too much (distance >= 0.2) set color to red
		mov_distance = np.linalg.norm(np.asarray(params) - np.asarray(old_params))

		glClearColor(0, 0.6, 0, 0.0)
		if mov_distance >= 0.2:
			glClearColor(1, 0.5, 0.5, 0.0)
		elif mov_distance < 0.2 and mov_distance > 0.1:
			glClearColor(0.6, 0.6, 0, 0.0)
		

		if option == 1:
			if mov_distance <= 0.1:
				brain = pichu_happy
			elif mov_distance < 0.2 and mov_distance > 0.1:
				brain = pichu_ok
			else:
				brain = pichu_sad



		#update screen
		
		glMatrixMode( GL_MODELVIEW )
		glLoadIdentity()


		glTranslatef(coords[1], -1*coords[0], -1*coords[2])
		
		glRotatef(coords[4]*rotation_scale, 1.0, 0.0, 0.0)
		glRotatef(coords[3]*rotation_scale*-1, 0.0, 1.0, 0.0)
		glRotatef(coords[5]*rotation_scale*-1, 0.0, 0.0, 1.0)


		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)


		glCallList(brain.gl_list)
			

		if option == 1:
			glMatrixMode( GL_MODELVIEW )
			glLoadIdentity()
			glCallList(body.gl_list)

		#keep the current paramenter for calculation distance in the next TR
		old_params = params

		pygame.display.flip()

conn.close()