from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, monitors,tools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding
import dotmot_params as par # experimental parameters

'''
SET UP EXPT
'''
#rename window for ease
win = par.win

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
expName = u'dotmot_stair'  # from the Builder filename that created this script
expInfo = {'participant':'', 'session':'001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# flag for 'escape' or other condition => quit the exp
endExpNow = False  
    
# Initialize components for Routine "trial"
trialClock = core.Clock()

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=u'/home/antonio/Desktop/WORKSPACE/projects/E01_phPIT_stim/dotmot.psyexp',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
    
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

# total num of trials
trialsN = 10 
trialCounter = 1
speed = 0.05
# timing for typical motion event
t_win = 0.06
# timing of motion event
t_targ = 0.5
# set max number of motion events
mte = 60
# set possible motion dir
# 0 = left to right 
# increasing angle rotates ccw
motion_dir = [0,45,90,135,180,225,270,315]

'''
START TRIALS
'''
while trialCounter <= trialsN:

    # set when the target event happens
    targ_event_loc = int(randint(30,high=mte,size=1))

   # draw fixations for 500ms
    par.fixation.draw()
    for pos in par.resp_pos:
        par.resp_sqr.pos = pos
        par.resp_sqr.draw()
    win.flip()
    core.wait(0.5)
    
    # present attention cue for 500ms
    par.fixation.draw()
    par.cue.draw()
    for pos in par.resp_pos:
        par.resp_sqr.pos = pos
        par.resp_sqr.draw()
    win.flip()
    core.wait(0.5)

    for num in range(mte):
        # reset trial clock
        t = trialClock.reset(); 
        t = trialClock.getTime()

        if num == targ_event_loc:
            t_mevent=t+t_targ
        else:
            # set motion event timing
            t_mevent= t+t_win
        
        # change dot direction - randomly chosen from motion dir list
        par.r_dots.dir= motion_dir[int(randint(len(motion_dir),size=1))]
        par.l_dots.dir= motion_dir[int(randint(len(motion_dir),size=1))]
        
        while t < t_mevent:
            # display fixation cross
            par.fixation.draw()
            
            # response locations
            for pos in par.resp_pos:
                par.resp_sqr.pos = pos
                par.resp_sqr.draw()
            
            # draw dot clouds
            par.r_dots.draw()
            par.l_dots.draw()
            win.flip()
            
            # set dot refresh --speed--
            #core.wait(speed)
            t = trialClock.getTime() 
            
            # quit if escape is pressed
            if event.getKeys(keyList=["escape"]):
                core.quit()
    
    # collect key presses
    
    
    # update trial counter
    trialCounter+=1