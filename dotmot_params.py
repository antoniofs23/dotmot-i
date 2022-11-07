from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, monitors,tools
import numpy as np

#turn eyetracking on or off
eyetracking=True

#total number of trials per session
trialsN = 10
speed_s  = 0.05

#timing 
t_win = 0.06 # timing for typical motion event
t_targ = 0.5  # timing of motion event
mte = 60      # set max number of motion events
cue_t=0.5   # timing of attention cue
fix_t   = 0.5  # timing for fixation cue

#screen params
# resolution [pix]
# refresh rate [Hz]
# distance [cm]
# width [cm]
scr = dict(resolution=(1024,768), refresh_rate=85,dist=57,width=30)

# fixation parameters
fix = dict(size=0.2, lineColor=[1,1,1], fillColor=[1,1,1],
opacity=1, depth=-3.0)

# cue parameters
cue_ = dict(length=0.1,width=0.6)

#stimulus parameters
dots = dict(
nDots = 200,
dotSiz= 2.0,
speed = speed_s,
coherence = 1,
direction = 45,
fieldSize = 2.75,
fieldShape = 'circle',
color=[1.0,1.0,1.0],
opacity=None,
depth=-1)

# number of repetitions of the basic 10 trials i.e. 4 = 40 trials
numreps=1

# possible motion direction
# 0 = left to right 
# increasing angle rotates ccw
motion_dir = [0,45,90,135,180,225,270,315]

# left vs right dot Field
# eccentricity in degrees
R_fieldPos = (6.5,0.0)
L_fieldPos = (-6.5,0.0)

# set up 8 response dots
resp_pos = [(12.5,0),(-12.5,0),
                     (0,10),(0,-10),
                     (9.5,8),(-9.5,8),
                     (-9.5,-8),(9.5,-8)]

# Setup the Window
win = visual.Window(
    size=scr['resolution'], fullscr=True, screen=1,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb', 
    blendMode='avg', useFBO=True)
    
# set up stim
# introduction Image
path_to_image="instruc.png"
image_stim=visual.ImageStim(win,image=path_to_image)

# right dot field
r_dots = visual.DotStim(
    win=win, units='deg',nDots=dots['nDots'], dotSize=dots['dotSiz'],
    speed=dots['speed'], dir=dots['direction'], coherence=1,
    fieldPos=R_fieldPos, fieldSize=dots['fieldSize'], fieldShape=dots['fieldShape'],
    signalDots='same', noiseDots='direction',dotLife=3.0,
    color=dots['color'], colorSpace='rgb', opacity=dots['opacity'],
    depth=dots['depth'])

# left dot field
l_dots = visual.DotStim(
    win=win, units='deg',nDots=dots['nDots'], dotSize=dots['dotSiz'],
    speed=dots['speed'], dir=dots['direction'], coherence=1,
    fieldPos=L_fieldPos, fieldSize=dots['fieldSize'], fieldShape=dots['fieldShape'],
    signalDots='same', noiseDots='direction',dotLife=3.0,
    color=dots['color'], colorSpace='rgb', opacity=dots['opacity'],
    depth=dots['depth'])

# response squre
resp_sqr = visual.Rect(
    win=win, units='deg',size=0.25,
    pos=(0,0),lineColor=fix['lineColor'],lineColorSpace='rgb',
    fillColor=fix['fillColor'], fillColorSpace='rgb',
    opacity=fix['opacity'], depth=fix['depth'],interpolate=True)

# fixation circle
fixation = visual.Circle(
    win=win, units='deg',size=0.1,
    pos=(0,0),lineColor=fix['lineColor'],lineColorSpace='rgb',
    fillColor=fix['fillColor'], fillColorSpace='rgb',
    opacity=fix['opacity'], depth=fix['depth'],interpolate=True)

# attention cue
cue_right = visual.ShapeStim(win,units='deg',
    vertices = [[-0.2,-0.1], [-0.2,0.1], [0.2,0]],
    pos=(0.45,0.0),lineColor = 'white', fillColor = 'white')
    
cue_left = visual.ShapeStim(win,units='deg',
    vertices = [[-0.2,-0.1], [-0.2,0.1], [0.2,0]],ori=180.0,
    pos=(-0.45,0.0),lineColor = 'white', fillColor = 'white')


    
    
