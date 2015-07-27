import os
import signal
import subprocess
import sys

from psychopy import visual, core
import numpy as np

SCALE = 0.4
LINE_WIDTH = 4.0

def draw_cross():
	#up
	stim1 = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	stim1.vertices = [[ -0.1*SCALE, 0.2*SCALE], [0.0*SCALE, 0.3*SCALE], [0.1*SCALE, 0.2*SCALE]]

	stim2 = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	stim2.vertices = [[ -0.1*SCALE, 0.3*SCALE], [0.0*SCALE, 0.4*SCALE], [0.1*SCALE, 0.3*SCALE]]


	#right
	stim3 = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	stim3.vertices = [[ 0.3*SCALE, -0.1*SCALE], [0.4*SCALE, 0.0*SCALE], [0.3*SCALE, 0.1*SCALE]]

	stim4 = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	stim4.vertices = [[ 0.2*SCALE, -0.1*SCALE], [0.3*SCALE, 0.0*SCALE], [0.2*SCALE, 0.1*SCALE]]


	#down
	stim5 = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	stim5.vertices = [[0.1*SCALE, -0.2*SCALE], [0.0*SCALE, -0.3*SCALE], [-0.1*SCALE, -0.2*SCALE]]

	stim6 = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	stim6.vertices = [[ 0.1*SCALE, -0.3*SCALE], [0.0*SCALE, -0.4*SCALE], [-0.1*SCALE, -0.3*SCALE]]


	#left
	stim7 = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	stim7.vertices = [[ -0.3*SCALE, 0.1*SCALE], [-0.4*SCALE, 0.0*SCALE], [-0.3*SCALE, -0.1*SCALE]]

	stim8 = visual.ShapeStim(win,lineWidth=LINE_WIDTH,closeShape=False)
	stim8.vertices = [[ -0.2*SCALE, 0.1*SCALE], [-0.3*SCALE, 0.0*SCALE], [-0.2*SCALE, -0.1*SCALE]]


	circle = visual.Circle(win, radius=0.05*SCALE, lineWidth=LINE_WIDTH)

	stims = [stim1, stim2, stim3, stim4, stim5,stim6, stim7, stim8, circle]

	for s in stims:
		s.draw()		

	return stims


def cross_pos(cross, x, y):
	for stim in cross:
		stim.pos = (x,y)
		stim.draw()



def cross_color(cross, color):
	for stim in cross:
		stim.lineColor = color
		stim.draw()


#TODO: 
	#change cross size
	#cross should be always on the screen
	#move cross smoothly (ouvir a porta em vez de pegar o output do terminal)


#start psychopy
win = visual.Window( [1024, 768] ,fullscr=False)#,mon='monitor_name' )
cross = draw_cross()
win.flip()



process = subprocess.Popen(['realtime_receiver.py', '-show_data', 'yes'], stdout=subprocess.PIPE)

old_mov_params = [0.0]*6

while True:

	#parse mov params
	line = process.stdout.readline()
	
	if 'recv motion' in line:
		new_mov_params = []

		mov_params = line[20:].split('   ')

		#parse floats
		for p in mov_params:
			try:
				new_mov_params.append(float(p))
			except ValueError:
				pass

			
		#sys.stdout.write(str(new_mov_params) + '\n')
		#sys.stdout.flush()


		###### update screen ######


		#update position x,y
		x_coord = new_mov_params[0]*10
		y_coord = new_mov_params[1]*10
		z_coord = new_mov_params[3]*10

		cross_pos(cross, y_coord, y_coord)


		#update position z (zoom cross in or out)
		print z_coord
		if z_coord > 0:
			


		# set cross color according to movment
		mov_distance = np.linalg.norm(np.asarray(new_mov_params) - np.asarray(old_mov_params))


		# set color to green if not moving
		new_color = [0.0, 1.0, 0.0]

		#set color to red when moving too much
		if mov_distance >= 0.2:
			new_color = [1.0, 0.0, 0.0]
		elif mov_distance < 0.2 and mov_distance > 0.1:
			new_color = [1.0, 1.0, 0.0] 

		cross_color(cross, new_color)


		old_mov_params = new_mov_params

		
		win.flip()



#++ recv motion:     0.00214    -0.00874   -0.24210   0.00675    -0.02543   0.02336 
#++ recv motion:     -0.03808   -0.02246   -0.08772   -0.01898   0.01214    0.00835
#++ recv motion:     -0.00000   0.00000    -0.00000   0.00000    0.00000    -0.00000 