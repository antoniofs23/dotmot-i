from psychopy import locale_setup, sound, gui, visual, core, data, event, logging,sound,monitors,tools,iohub,hardware
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding
import time
import dotmot_params as par # experimental parameters
import pupilcore as ep # eyetracking code
from psychopy.hardware import keyboard
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

# beeps for correct responses
beep = sound.Sound(value='A')
'''
EYE-TRACKING
'''
if par.eyetracking:
    # instantiate eyetracking class
    eyeTracker = ep.eyeTracking(par.scr['resolution'],par.scr['dist'], par.scr['width'], ip= '127.0.0.1',port='50020')
    # initialize eye-tracking connection
    eyeTracker.init_connect()
    # start-recording
    eyeTracker.start_recording(filename)
    # start-calibration
    eyeTracker.start_calibration()
    # open ports to communicate with pupil
    eyeTracker.open_speak_port()
    # open listen port
    eyeTracker.open_listen_port()
    #setup eye-tracking clock
    # measure clock offset
    stable_offset_mean = eyeTracker.measure_clock_offset_stable(trialClock.getTime,n_samples=10)
    #pupil_time_actual = eyeTracker.request_pupil_time()
    #local_time_actual = trialClock.getTime()
    #pupil_time_calc_locally = local_time_actual + stable_offset_mean
    # prepare to send annotations
    eyeTracker.notify({'subject': 'start_plugin', 'name': 'Annotation_Capture', 'args': {}})
    
    
    

    
# Instructions screen
par.image_stim.draw()
win.flip()
event.waitKeys() # press space to continue

'''
START TRIALS
'''
for  thisTrial in trials:
        # send trial start trigger
        t = trialClock.reset()
        t = trialClock.getTime()
        if par.eyetracking:
            trigger1=ep.eyeTracking.new_trigger('trial_start',0.0,t+stable_offset_mean)
            eyeTracker.send_trigger(trigger1)
        
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
        
        # pre-cue offset
        t = trialClock.getTime()
        if par.eyetracking:
            trigger1=ep.eyeTracking.new_trigger('pre_cue_offset',0.0,t+stable_offset_mean)
            eyeTracker.send_trigger(trigger1)
                    
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
            
            # start of motion event
            t = trialClock.getTime()
            if par.eyetracking:
                trigger1=ep.eyeTracking.new_trigger('motion_event_onset',0.0,t+stable_offset_mean)
                eyeTracker.send_trigger(trigger1)
            while t < t_mevent:                    
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
            
                # start of motion event
                t = trialClock.getTime()
                if par.eyetracking:
                    trigger1=ep.eyeTracking.new_trigger('motion_event_offset',0.0,t+stable_offset_mean)
                    eyeTracker.send_trigger(trigger1)
                
        # store data
        trials.addData('targ_event_idx',targ_event_loc)
        thisExp.nextEntry()

if par.eyetracking:
    # end recording
    core.wait(3) # wait 3 secs
    eyeTracker.end_recording()