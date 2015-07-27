import os
import signal
import subprocess
import sys
import socket
import struct

from psychopy import visual, core
import numpy as np

SCALE = 0.4
LINE_WIDTH = 4.0

def draw_cross(scale):
	#up
	stim1 = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	stim1.vertices = [[ -0.1*scale, 0.2*scale], [0.0*scale, 0.3*scale], [0.1*scale, 0.2*scale]]

	stim2 = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	stim2.vertices = [[ -0.1*scale, 0.3*scale], [0.0*scale, 0.4*scale], [0.1*scale, 0.3*scale]]


	#right
	stim3 = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	stim3.vertices = [[ 0.3*scale, -0.1*scale], [0.4*scale, 0.0*scale], [0.3*scale, 0.1*scale]]

	stim4 = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	stim4.vertices = [[ 0.2*scale, -0.1*scale], [0.3*scale, 0.0*scale], [0.2*scale, 0.1*scale]]


	#down
	stim5 = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	stim5.vertices = [[0.1*scale, -0.2*scale], [0.0*scale, -0.3*scale], [-0.1*scale, -0.2*scale]]

	stim6 = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	stim6.vertices = [[ 0.1*scale, -0.3*scale], [0.0*scale, -0.4*scale], [-0.1*scale, -0.3*scale]]


	#left
	stim7 = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	stim7.vertices = [[ -0.3*scale, 0.1*scale], [-0.4*scale, 0.0*scale], [-0.3*scale, -0.1*scale]]

	stim8 = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	stim8.vertices = [[ -0.2*scale, 0.1*scale], [-0.3*scale, 0.0*scale], [-0.2*scale, -0.1*scale]]


	circle = visual.Circle(win, radius=0.05*scale, lineWidth=LINE_WIDTH)

	stims = [stim1, stim2, stim3, stim4, stim5,stim6, stim7, stim8, circle]		

	return stims

def cross_pos(cross, x, y):
	for stim in cross:
		stim.pos = (x,y)

def cross_color(cross, color):
	for stim in cross:
		stim.lineColor = color

def cross_clear(cross):
	for stim in cross:
		del(stim)
	del(cross)


#TODO: 
	#change axis


#start psychopy
old_params = [0.0]*6
win = visual.Window( [1024, 768] ,fullscr=False)#,mon='monitor_name' )
cross = draw_cross(SCALE)

for stim in cross:
	stim.draw()

win.flip()


TCP_IP = '127.0.0.1'
TCP_PORT = 53214
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((TCP_IP, TCP_PORT))

s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr



while 1:

	data = conn.recv(BUFFER_SIZE)
	if not data: break

	###### receive 6 mov params ######
	if len(data) == 24:

		#clean screen, delete cross
		#cross_clear(cross)


		params = []
		for i in range(6):
			param = struct.unpack('f',  data[i*4:i*4+4])[0]
			params.append(param)


		###### update screen ######
		x_coord = params[0]*10
		y_coord = params[1]*10
		z_coord = params[3]*10

		#update position z (zoom cross in or out)
		scale = SCALE
		if z_coord > 0:
			scale = SCALE + z_coord
		elif z_coord < 0:
			scale = SCALE - z_coord


		if scale > 0.8:
			scale = 0.8
		if scale < 0.3:
			scale = 0.3


		cross = draw_cross(scale)



		#don't allow cross to leave screen
		if x_coord > 0.85:
			x_coord = 0.85
		if x_coord < -0.85:
			x_coord = -0.85

		if y_coord > 0.85:
			y_coord = 0.85
		if y_coord < -0.85:
			y_coord = 0.85

		cross_pos(cross, y_coord, y_coord)
		



		###### set cross color according to movment ######
		mov_distance = np.linalg.norm(np.asarray(params) - np.asarray(old_params))


		# set color to green if not moving
		new_color = [0.0, 1.0, 0.0]

		#set color to red when moving too much
		if mov_distance >= 0.2:
			new_color = [1.0, 0.0, 0.0]
		elif mov_distance < 0.2 and mov_distance > 0.1:
			new_color = [1.0, 1.0, 0.0] 

		cross_color(cross, new_color)


		old_params = params

		for stim in cross:
			stim.draw()

		win.flip()



#++ recv motion:     0.00214    -0.00874   -0.24210   0.00675    -0.02543   0.02336 
#++ recv motion:     -0.03808   -0.02246   -0.08772   -0.01898   0.01214    0.00835
#++ recv motion:     -0.00000   0.00000    -0.00000   0.00000    0.00000    -0.00000 