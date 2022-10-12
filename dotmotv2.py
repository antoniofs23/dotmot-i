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

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
expName = u'dotmotv2'  # from the Builder filename that created this script
expInfo = {'participant':'', 'session':'001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Setup the Window
win = visual.Window(
    size=par.scr['resolution'], fullscr=False, screen=0,
    allowGUI=True, allowStencil=False,
    monitor='psychophysicsRoom_Monitor', color=[0,0,0], colorSpace='rgb', 
    blendMode='avg', useFBO=True)

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

'''
SET UP STIMULI
'''
# can update the stim parameters in the experiment
r_dots = visual.DotStim(
    win=win, units='deg',nDots=par.dots['nDots'], dotSize=par.dots['dotSiz'],
    speed=par.dots['speed'], dir=par.dots['direction'], coherence=par.dots['coherence'],
    fieldPos=par.R_fieldPos, fieldSize=par.dots['fieldSize'], fieldShape=par.dots['fieldShape'],
    signalDots='same', noiseDots='direction',dotLife=3.0,
    color=par.dots['color'], colorSpace='rgb', opacity=par.dots['opacity'],
    depth=-par.dots['depth'])
    
l_dots = visual.DotStim(
    win=win, units='deg',nDots=par.dots['nDots'], dotSize=par.dots['dotSiz'],
    speed=par.dots['speed'], dir=par.dots['direction'], coherence=par.dots['coherence'],
    fieldPos=par.L_fieldPos, fieldSize=par.dots['fieldSize'], fieldShape=par.dots['fieldShape'],
    signalDots='same', noiseDots='direction',dotLife=3.0,
    color=par.dots['color'], colorSpace='rgb', opacity=par.dots['opacity'],
    depth=-par.dots['depth'])

resp_sqr = visual.Rect(
    win=win, units='deg',size=0.25,
    pos=(0,0),lineColor=par.fix['lineColor'],lineColorSpace='rgb',
    fillColor=par.fix['fillColor'], fillColorSpace='rgb',
    opacity=par.fix['opacity'], depth=par.fix['depth'],interpolate=True)
    
fixation = visual.Circle(
    win=win, units='deg',size=0.1,
    pos=(0,0),lineColor=par.fix['lineColor'],lineColorSpace='rgb',
    fillColor=par.fix['fillColor'], fillColorSpace='rgb',
    opacity=par.fix['opacity'], depth=par.fix['depth'],interpolate=True)

cue = visual.Line(
    win=win, units='deg', start=(0,0), end= (par.cue['length'],0),
    lineWidth=par.cue['width'],lineColor='white',pos=(0.25,0))

'''
TIMING
'''
globalClock = core.Clock()
routineTimer=core.CountdownTimer()

# --------Prepare to start Staircase "trials" --------
# set up handler to look after next chosen value etc
trials = data.StairHandler(startVal=0.5, extraInfo=expInfo,
    stepSizes=[0.4, 0.2, 0.2, 0.1], stepType='log',
    nReversals=0, nTrials=50, 
    nUp=1, nDown=3,
    minVal=0, maxVal=1,
    originPath=-1, name='trials')

thisExp.addLoop(trials)  # add the loop to the experiment
level = thisTrial = 0.5  # initialise some vals

for thisTrial in trials:
    currentLoop = trials
    level = thisTrial
    
    # ------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    if random() > 0.5:
        corrAns = 'up'
        direction = 90
    else:
        corrAns = 'down'
        direction = -90
    
    thisExp.addData('corrAns', corrAns)
    thisExp.addData('direction', direction)
    r_dots.setFieldCoherence(level);   l_dots.setFieldCoherence(level)
    r_dots.setDir(direction);     l_dots.setDir(direction)
    r_dots.refreshDots();     l_dots.refreshDots()
    resp = event.BuilderKeyResponse()
    # keep track of which components have finished
    trialComponents = [r_dots,l_dots, resp, fixation]
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # fixation cross
    fixation.draw()
    
    # update and display attention cue
    cue.draw()
    
    win.flip()
    core.wait(500/1000)
    # -------Start Routine "trial"-------
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # *dots* updates
        if t >= 0.5 and r_dots.status == NOT_STARTED:
            # keep track of start time/frame for later
            r_dots.tStart = t;  l_dots.tStart = t
            r_dots.frameNStart = frameN;   l_dots.frameNStart = frameN# exact frame index
            r_dots.setAutoDraw(True);  l_dots.setAutoDraw(True)
        frameRemains = 0.5 + 1.0- win.monitorFramePeriod * 0.75  # most of one frame period left
        if r_dots.status == STARTED and t >= frameRemains:
            r_dots.setAutoDraw(False);   l_dots.setAutoDraw(False)
        
        # *resp* updates
        if t >= 0.5 and resp.status == NOT_STARTED:
            # keep track of start time/frame for later
            resp.tStart = t
            resp.frameNStart = frameN  # exact frame index
            resp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(resp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if resp.status == STARTED:
            theseKeys = event.getKeys(keyList=['up', 'down'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                if resp.keys == []:  # then this was the first keypress
                    resp.keys = theseKeys[0]  # just the first key pressed
                    resp.rt = resp.clock.getTime()
                    # was this 'correct'?
                    if (resp.keys == str(corrAns)) or (resp.keys == corrAns):
                        resp.corr = 1
                    else:
                        resp.corr = 0
                    # a response ends the routine
                    continueRoutine = False
        
        # *fixation* updates
        if t >= 0.0 and fixation.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixation.tStart = t
            fixation.frameNStart = frameN  # exact frame index
            fixation.setAutoDraw(True)
        
        # draw response circles
        for pos in par.resp_pos:
                resp_sqr.pos = pos
                resp_sqr.draw()
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # check responses
    if resp.keys in ['', [], None]:  # No response was made
        resp.keys=None
        # was no response the correct answer?!
        if str(corrAns).lower() == 'none':
           resp.corr = 1  # correct non-response
        else:
           resp.corr = 0  # failed to respond (incorrectly)
    # store data for trials (StairHandler)
    trials.addResponse(resp.corr)
    trials.addOtherData('resp.rt', resp.rt)
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()