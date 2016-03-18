import socket
import struct

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
import math
import objloader as loader

import os
import sys
import select
import threading

from psychopy import core


import OpenGL.GL as ogl  
def draw_text(position, text, last_color): 
    font = pygame.font.Font (None, 64)
    textSurface = font.render(text, True, (255,255,255,255), last_color )     
    textData = pygame.image.tostring(textSurface, "RGBA", True)    
    glRasterPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)



coord_scale = 0.1
rotation_scale = 1.5


instructions = [
    'It is very important that you keep',
    'your head still during the MRI scan.',
    'This game will show you how much your',
    'head moves using a 3D cartoon. When',
    'your head moves, the cartoon will move.', 
    'The background will change color based on',
    'how much your head moves. Green is good',
    'and Red is too much.',
    ' ',
    'To play the game, tell the operator which',
    'cartoon you would like to be and then ',
    'follow the instructions at the bottom of the screen.'
    ]


###### start psychopy ######
#creates a full screen window and draw a white cross on the screen while waiting for inputs
############################
pygame.init()

screen_info = pygame.display.Info()

display = (screen_info.current_w, screen_info.current_h)
screen = pygame.display.set_mode(display, DOUBLEBUF|FULLSCREEN)

#show instructions
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))


for i in range(len(instructions)):
    font = pygame.font.Font(None, 64)
    text = font.render(instructions[i], 1, (255,255,255,255))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = 192 + 50*i
    background.blit(text, textpos)

    # Blit everything to the screen
    screen.blit(background, (0, 0))

pygame.display.flip()


while True:
    stop = False
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_1):
            stop = True

    if stop:
        font = None
        background = None
        break


screen = pygame.display.set_mode(display, DOUBLEBUF|FULLSCREEN)

#show menu

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




screen = pygame.display.set_mode(display, DOUBLEBUF|FULLSCREEN)

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

obj_name = 'pichu'
if option == 2:
    obj_name = 'the plane'
elif option == 3:
    obj_name = 'the brain'


texts = [
    {'text':'Move your head and watch '+ obj_name +' follow you', 'time': 20, 'offset': -0.28},
    {'text':'Now practice staying still', 'time': 20, 'offset':-0.15},
    {'text':'Cough', 'time': 5, 'offset':-0.035},
    {'text':'Wiggle your feet', 'time': 5, 'offset':-0.1},
    {'text':'Move your hands', 'time': 5, 'offset':-0.1},
    {'text':'See how these small things move your head?', 'time': 5, 'offset':-0.28},
    {'text':'Practice staying very still', 'time': 30, 'offset':-0.15}
    ]

pichu = None
plane = None
brain = None
screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL|FULLSCREEN)
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
    pichu_happy = loader.OBJ('pichu/pichu_smile.obj', swapyz=True)
    pichu_ok = loader.OBJ('pichu/pichu_ok.obj', swapyz=True)
    pichu_sad = loader.OBJ('pichu/pichu_sad.obj', swapyz=True)
    zoom = -0.6
    brain = pichu_happy
    glTranslatef(0.0,0.0, zoom)


# #if plane
elif option == 2:
    zoom = -1
    brain = loader.OBJ('plane9.obj', swapyz=True)
    glTranslatef(0.0,0.0, zoom)
    


#if brain
else:
    zoom = -1
    glMaterialfv(GL_FRONT, GL_SPECULAR,  (1.0, 1.0, 1.0, 50.0))
    glMaterialfv(GL_FRONT, GL_SHININESS, (50.0))
    glColor([1.0,0.4,0.6])
    brain = loader.OBJ('brain18.obj', swapyz=True)

    glTranslatef(0.0,0.0, zoom)


text_index = 0


glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

glCallList(brain.gl_list)

pygame.display.flip()
print('finish loading')

import datetime

log_file = open('motion' + datetime.datetime.now().strftime("%Y-%m-%d%H%M") +'.log', 'wb')
if option == 1:
    log_file.write('Pichu\n')
elif option == 2:
    log_file.write('plane\n')
else:
    log_file.write('brain\n')
    
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

# make the socket non-blocking
s.setblocking(0)

s.bind((TCP_IP, TCP_PORT))
s.listen(1)

SOCKETCONNECTEVENT = USEREVENT + 0

def socket_connection_handler(sock):
    event = pygame.event.Event(SOCKETCONNECTEVENT, {'socket':sock})
    r,w,x = select.select([sock],[],[])
    pygame.event.post(event)

sock_thread = threading.Thread(target=socket_connection_handler,args=(s,))
sock_thread.start()

print 'connecting'

# use select to wait for a connection
# or a keypress, whichever comes first
while True:
    
        event = pygame.event.wait()
        
        if event.type == SOCKETCONNECTEVENT:
            conn, addr = s.accept()
            conn.setblocking(0)
            sock_thread.join()
            break
            
        if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
            s.close()
            log_file.close()
            pygame.quit()
            sys.exit()

old_params = [0.0]*6

###### now things are actually happening ######
# enters in the while loop when the sender is ready.
# parses the movement paramenters and update the screen accordingly
# exit when not receiving more data
############################
clock = core.Clock()
text_index = 0
last_color = (0,0,0,0)

while True:
    #event = pygame.event.wait()
    if clock.getTime() >= texts[text_index]['time']:
        if text_index < len(texts) - 1:
            text_index += 1
            clock.reset()

            if option == 1:
                draw_text([texts[text_index]['offset'],-0.15,0.0],texts[text_index]['text'], last_color)
            else:
                draw_text([texts[text_index]['offset']*1.7,-0.25,0.0],texts[text_index]['text'], last_color)




    for event in pygame.event.get():

        if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
            log_file.close()
            pygame.quit()
            sys.exit()


    data = [0.0]*6
    try:
        data = conn.recv(CONTROL_SIZE)
    except socket.error as ex:
        continue


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
        
        log_file.write(str(params)[1:-1] + '\n')

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
        mov_distance = np.linalg.norm(np.asarray(params[:3]) - np.asarray(old_params[:3]))+\
            80*2*np.pi*(np.linalg.norm(np.asarray(params[3:]) - np.asarray(old_params[3:]))/360)
        print "moved %f mm"%(mov_distance)

        glClearColor(0, 0.6, 0, 0.0)
        last_color = (0, 0.6*255, 0, 255)
        if mov_distance >= 0.2:
            glClearColor(1, 0.5, 0.5, 0.0)
            last_color = (255, 0.5*255, 255*0.5, 255)
        elif mov_distance < 0.2 and mov_distance > 0.1:
            glClearColor(0.6, 0.6, 0, 0.0)
            last_color = (0.6*255, 0.6*255, 0, 255)


        if option == 1:
            if mov_distance <= 0.2:
                brain = pichu_happy
            elif mov_distance < 0.3 and mov_distance > 0.2:
                brain = pichu_ok
            else:
                brain = pichu_sad


        #update screen

        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()


        glTranslatef(-1*coords[1], coords[0], coords[2])

        glRotatef(coords[4]*rotation_scale, 1.0, 0.0, 0.0)
        glRotatef(coords[3]*rotation_scale*-1, 0.0, 1.0, 0.0)
        glRotatef(coords[5]*rotation_scale*-1, 0.0, 0.0, 1.0)


        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)


        glCallList(brain.gl_list)

        #keep the current paramenter for calculation distance in the next TR
        old_params = params

        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()
        if option == 1:
            draw_text([texts[text_index]['offset'],-0.15,0.0],texts[text_index]['text'], last_color)
        else:
            draw_text([texts[text_index]['offset']*1.7,-0.25,0.0],texts[text_index]['text'], last_color)


        pygame.display.flip()

conn.close()
log_file.close()