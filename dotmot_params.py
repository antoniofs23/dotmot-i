#screen params
scr = dict(resolution=(1024,768), refresh_rate=85)

# fixation parameters
fix = dict(size=0.2, lineColor=[1,1,1], fillColor=[1,1,1],
opacity=1, depth=-3.0)

# cue parameters
cue = dict(length=0.1,width=0.6)

#stimulus parameters
dots = dict(
nDots = 100,
dotSiz= 4.0,
speed = 0.08,
coherence = 1,
direction = 0.0,
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


