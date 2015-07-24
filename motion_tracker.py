import os
import signal
import subprocess
import sys

from psychopy import visual, core
import numpy

SCALE = 1000

#TODO: 
		#change cross color
		#change cross size
		#cross should be always on the screen
		#move cross smoothly

#start psychopy
win = visual.Window( [1024, 768] ,fullscr=True, units='pix')#,mon='monitor_name' )
cross = visual.TextStim(win, text='X')
cross.setAutoDraw(True)
win.flip()


process = subprocess.Popen(['realtime_receiver.py', '-show_data', 'yes'], stdout=subprocess.PIPE)

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

			
		sys.stdout.write(str(new_mov_params) + '\n')
		sys.stdout.flush()


		#update screen
		x_coord = new_mov_params[0]*SCALE
		y_coord = new_mov_params[1]*SCALE

		cross.pos = [y_coord, y_coord]
		win.flip()



#++ recv motion:     0.00214    -0.00874   -0.24210   0.00675    -0.02543   0.02336 
#++ recv motion:     -0.03808   -0.02246   -0.08772   -0.01898   0.01214    0.00835
#++ recv motion:     -0.00000   0.00000    -0.00000   0.00000    0.00000    -0.00000 