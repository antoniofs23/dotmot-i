from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, monitors,tools,sound,iohub,hardware
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding
import dotmot_params as par # experimental parameters
from psychopy.hardware import keyboard
#import psychopy.iohub.devices.eyetracker.hw.pupil_labs.pupil_core as pc
#import psychopy.iohub as io
#import zmq  #eye-tracking lib
#from msgpack import loads

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
trials = data.TrialHandler(trialList=data.importConditions('conditions.csv'), nReps=par.numreps)

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expInfo['session'], expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='1.0', extraInfo=expInfo, dataFileName=filename)

# add trials to handler
thisExp.addLoop(trials)

'''
EYE-TRACKING
'''
if par.eyetracking:
    ctx=zmq.Context()
    pupil_remote=ctx.socket(zmq.REQ)
    pupil_remote.connect('tcp://127.0.0.1:50020')
    
    #start recording
    pupil_remote.send_string('R '+filename)
    print(pupil_remote.recv_string())
    
    # start calibration
    pupil_remote.send_string('C')
    print(pupil_remote.recv_string())
    
    # ask for sub port
    pupil_remote.send_string('SUB_PORT')
    sub_port = pupil_remote.recv_string()
    
    #open sub port to listen pupil
    sub = ctx.socket(zmq.SUB)
    sub.connect("tcp://{}:{}".format('127.0.0.1', sub_port))
    sub.subscribe('gaze.')
    
    
# Instructions screen
par.image_stim.draw()
win.flip()
event.waitKeys() # press space to continue

mySound=sound.Sound('A')

'''
START TRIALS
'''
for  thisTrial in trials:
    #get gaze position
        topic, msg = sub.recv_multipart()
        gaze_position = loads(msg, raw=False)
        
       # test eye-tracking
        loc = gaze_position['norm_pos']
        pix_loc = (loc[0]*640,loc[1]*480)
        deg = par.pix2deg(par.scr,pix_loc)
        polar_ang = par.polarang(a=deg[0],b=deg[1])
        print(polar_ang)
    
        # beep at the start of the trial
        mySound.play()
        
        # set when the target event happens
        targ_event_loc = int(randint(30,high=par.mte,size=1))
        
       # draw fixations for 500ms
        par.fixation.draw()
        for loc in par.resp_pos:
            par.resp_sqr.pos= loc
            par.resp_sqr.draw()
        win.flip()
        core.wait(par.fix_t)
        par.fixation.draw()
        for loc in par.resp_pos:
            par.resp_sqr.pos= loc
            par.resp_sqr.draw()
        
        # present attention cue for 500ms
        # valid 
        if thisTrial['attention_cue']=='valid':
            if thisTrial['target_loc']=='left':
                par.cue_left.draw()
            else:
                par.cue_right.draw()
            
        # neutral 
        if thisTrial['attention_cue']=='neutral':
            par.cue_right.draw()
            par.cue_left.draw()
        
        win.flip()
        core.wait(par.cue_t)

        for num in range(par.mte):
            # reset trial clock
            t = trialClock.reset()
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
                #get gaze position
                #topic, msg = sub.recv_multipart()
                #gaze_position = loads(msg, raw=False)
                 
                #to go from norm_pos to pixel space multiply by screen res
                #loc = gaze_position['norm_pos']
                #pix_loc = (loc[0]*640,loc[1]*480)
                #deg = par.pix2deg(par.scr,pix_loc)
                #polar_ang = par.polarang(a=deg[0],b=deg[1])
                #print(polar_ang)
                # display fixation cross
                par.fixation.draw()
                for loc in par.resp_pos:
                    par.resp_sqr.pos= loc
                    par.resp_sqr.draw()
                
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
                
                # store data
        trials.addData('targ_event_idx',targ_event_loc)
        thisExp.nextEntry()

# end recording
core.wait(3) # wait 3 secs
pupil_remote.send_string('r') # end recording
