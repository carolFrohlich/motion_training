import socket
import struct
from psychopy import visual, core
import numpy as np

SCALE = 0.4
LINE_WIDTH = 4.0
coord_scale=2

def build_cross(scale):
	#up
	up_in = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	up_in.vertices = [[ -0.1*scale, 0.2*scale], [0.0*scale, 0.3*scale], [0.1*scale, 0.2*scale]]

	up_out = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	up_out.vertices = [[ -0.1*scale, 0.3*scale], [0.0*scale, 0.4*scale], [0.1*scale, 0.3*scale]]

	#right
	right_in = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	right_in.vertices = [[ 0.2*scale, -0.1*scale], [0.3*scale, 0.0*scale], [0.2*scale, 0.1*scale]]

	right_out = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	right_out.vertices = [[ 0.3*scale, -0.1*scale], [0.4*scale, 0.0*scale], [0.3*scale, 0.1*scale]]

	#down
	down_in = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	down_in.vertices = [[0.1*scale, -0.2*scale], [0.0*scale, -0.3*scale], [-0.1*scale, -0.2*scale]]

	down_out = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	down_out.vertices = [[ 0.1*scale, -0.3*scale], [0.0*scale, -0.4*scale], [-0.1*scale, -0.3*scale]]

	#left
	left_in = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	left_in.vertices = [[ -0.2*scale, 0.1*scale], [-0.3*scale, 0.0*scale], [-0.2*scale, -0.1*scale]]

	left_out = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	left_out.vertices = [[ -0.3*scale, 0.1*scale], [-0.4*scale, 0.0*scale], [-0.3*scale, -0.1*scale]]


	circle = visual.Circle(win, radius=0.05*scale, lineWidth=LINE_WIDTH)
	cross = [up_in, up_out, right_in, right_out, down_in, down_out, left_in, left_out, circle]		

	return cross

def cross_pos(cross, x, y):
	for stim in cross:
		stim.pos = (x,y)

def cross_color(cross, color):
	for stim in cross:
		stim.lineColor = color

def cross_draw(cross):
	for stim in cross:
		stim.draw()


###### start psychopy ######
#creates a full screen window and draw a white cross on the screen while waiting for inputs
############################
win = visual.Window( [1024, 768], fullscr=False)
cross = build_cross(SCALE)
cross_draw(cross)
win.flip()


###### start socket ######
#Listens the port in which afni rt will send the movement parameters.
#The default values for running afni rt locally are: ip=127.0.0.1 and port=53214
#for running on the server: ip=0.0.0.0 and port=8000
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

		#scale the x,y and coordinates. 
		x_coord = params[0]*coord_scale
		y_coord = params[1]*coord_scale
		z_coord = params[3]*coord_scale


		#update position y (zoom cross in or out). 
		#Don'd let the cross gets too beg or too small
		scale = SCALE + y_coord

		if scale > 0.7:
			scale = 0.7
		if scale < 0.1:
			scale = 0.1

		cross = build_cross(scale)


		#update cross screen using x and z coords
		#and don't let the cross leave the screen
		if x_coord > 0.85:
			x_coord = 0.85
		if x_coord < -0.85:
			x_coord = -0.85

		if z_coord > 0.85:
			z_coord = 0.85
		if z_coord < -0.85:
			z_coord = 0.85

		cross_pos(cross, y_coord, y_coord)
		

		###### set cross color according to movment ######
		#calculates distance between last frame head position and current head position.
		# If participant is almost not moving (distance is <0.1) set color to green
		#if movment is between 0.1 and 0.1, set color to yelow.
		#and if participant is moving too much (distance >= 0.2) set color to red
		mov_distance = np.linalg.norm(np.asarray(params) - np.asarray(old_params))

		new_color = [0.0, 1.0, 0.0]
		if mov_distance >= 0.2:
			new_color = [1.0, 0.0, 0.0]
		elif mov_distance < 0.2 and mov_distance > 0.1:
			new_color = [1.0, 1.0, 0.0] 

		cross_color(cross, new_color)


		#keep the current paramenter for calculation distance in the next TR
		old_params = params

		#update screen
		cross_draw(cross)
		win.flip()
