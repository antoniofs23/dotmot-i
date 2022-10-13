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
expName = u'dotmot'  # from the Builder filename that created this script
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

# import condition file
#IMPORTANT: IF RUNNING ON UBUNTU--ONLY TAKES .CSV
trials = data.TrialHandler(trialList=data.importConditions('conditions.csv'), nReps=1)

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='1.0', extraInfo=expInfo, dataFileName=filename)

# add trials to handler
thisExp.addLoop(trials)
'''
START TRIALS
'''
for  thisTrial in trials:
    # set when the target event happens
    targ_event_loc = int(randint(30,high=par.mte,size=1))
    
   # draw fixations for 500ms
    par.fixation.draw()
    win.flip()
    core.wait(par.fix_t)
    
    # present attention cue for 500ms
    # valid [1]
    par.fixation.draw()
    if thisTrial['target_loc']=='right' and thisTrial['attention_cue']=='valid':
        par.cue.end = (par.cue_['length'],0); par.cue.draw()
    if thisTrial['target_loc']=='left' and thisTrial['attention_cue']=='valid':
        par.cue.start = (-0.1,0); par.cue.end=(0,0); par.cue.draw()
        
    #invalid [-1]
    if thisTrial['target_loc']=='right' and thisTrial['attention_cue']=='invalid':
        par.cue.start = (-0.1,0); par.cue.end=(0,0); par.cue.draw()
    if thisTrial['target_loc']=='left' and thisTrial['attention_cue']=='invalid':
        par.cue.end = (par.cue_['length'],0); par.cue.draw()
    
    # neutral [0]
    if thisTrial['attention_cue']=='neutral':
        par.cue.end = (par.cue_['length'],0); par.cue.draw()   
        par.cue.start = (-0.1,0); par.cue.end=(0,0); par.cue.draw()
    
    win.flip()
    core.wait(par.cue_t)

    for num in range(par.mte):
        # reset trial clock
        t = trialClock.reset(); 
        t = trialClock.getTime()
        
        # change dot direction - randomly chosen from motion dir list
        par.r_dots.dir= par.motion_dir[int(randint(len(par.motion_dir),size=1))]
        par.l_dots.dir= par.motion_dir[int(randint(len(par.motion_dir),size=1))]
        
        # set motion event timing
        # change motion event timing depending on target or not
        if num == targ_event_loc:
            t_mevent=t+par.t_targ
            trials.addData('left_dot_dir',par.l_dots.dir)
            trials.addData('right_dot_dir',par.r_dots.dir)
        else:
            t_mevent= t+par.t_win
            
        
        while t < t_mevent:
            # display fixation cross
            par.fixation.draw()
            
            # draw dot clouds
            par.r_dots.draw()
            par.l_dots.draw()
            win.flip()
            
            # set dot refresh --speed--
            #core.wait(speed)
            t = trialClock.getTime() 
            # record key presses
            keys = event.getKeys()
            if keys:
                if 'escape' in keys:
                    core.quit()
                #elif len(keys)==2:
                    #thisExp.addData('keys',' '.join(keys)
                    #thisExp.addData('RT',t)
                    
            # store data
    trials.addData('targ_event_idx',targ_event_loc)
    thisExp.nextEntry()
    
    
    # collect key presses
    
    