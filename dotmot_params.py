from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, monitors,tools

#
#screen params
scr = dict(resolution=(1024,768), refresh_rate=85)

# fixation parameters
fix = dict(size=0.2, lineColor=[1,1,1], fillColor=[1,1,1],
opacity=1, depth=-3.0)

# cue parameters
cue = dict(length=0.1,width=0.6)

#stimulus parameters
dots = dict(
nDots = 200,
dotSiz= 4.0,
speed = 0.08,
coherence = 1,
direction = 45,
fieldSize = 2.25,
fieldShape = 'circle',
color=[1.0,1.0,1.0],
opacity=None,
depth=-1)

# left vs right dot Field
# eccentricity in degrees
R_fieldPos = (4.5,0.0)
L_fieldPos = (-4.5,0.0)

# set up 8 response dots
resp_pos = [(8.5,0),(-8.5,0),
                     (0,6),(0,-6),
                     (5.5,4),(-5.5,4),
                     (-5.5,-4),(5.5,-4)]

# Setup the Window
win = visual.Window(
    size=scr['resolution'], fullscr=False, screen=0,
    allowGUI=True, allowStencil=False,
    monitor='psychophysicsRoom_Monitor', color=[0,0,0], colorSpace='rgb', 
    blendMode='avg', useFBO=True)
    
# set up stim
# right dot field
r_dots = visual.DotStim(
    win=win, units='deg',nDots=dots['nDots'], dotSize=dots['dotSiz'],
    speed=0.02, dir=dots['direction'], coherence=1,
    fieldPos=R_fieldPos, fieldSize=dots['fieldSize'], fieldShape=dots['fieldShape'],
    signalDots='same', noiseDots='direction',dotLife=3.0,
    color=dots['color'], colorSpace='rgb', opacity=dots['opacity'],
    depth=dots['depth'])

# left dot field
l_dots = visual.DotStim(
    win=win, units='deg',nDots=dots['nDots'], dotSize=dots['dotSiz'],
    speed=0.02, dir=dots['direction'], coherence=1,
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
cue = visual.Line(
    win=win, units='deg', start=(0,0), end=(cue['length'],0),
    lineWidth=cue['width'],lineColor='white',pos=(0.25,0))


        


