#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

from psychopy import gui, visual, core, data, event, logging, monitors
from numpy.random import choice as randchoice
import os 
import psychopy.iohub as io
from psychopy.hardware import keyboard
from experiment import Experiment


def runExperiment():
    # Ensure that relative paths start from the same directory as this script
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)

    # Store info about the experiment session
    psychopyVersion = '2022.1.3'
    expName = 'PsychoPyEEGTemplate'
    
    # Initialize Experiment object
    exp = Experiment()

    # If not run on the lab PC, ask for info required for visual angle calculation
    if exp.distributed_ver:
        monDW = {'Your distance to the screen in millimeters:': 570,
                   'The width of your screen in millimeters:': 310}
        
        dlgmon = gui.DlgFromDict(dictionary=monDW,
                               sortKeys=False, title=expName)
        
        if dlgmon.OK == False:
            core.quit()

        exp.monitor = monitors.Monitor("ExpMonitor", width=monDW['The width of your screen in millimeters:'],
                               distance=monDW['Your distance to the screen in millimeters:']) # sets up the monitor
    
    # Remind the experimenter to measure participant's distance to the screen    
    dist = exp.monitor.currentCalib["distance"]
    confirmDist = {f'The participant sits {dist} mm away from the monitor?': ['Yes', 'No']}
    dlgc = gui.DlgFromDict(dictionary=confirmDist, sortKeys=False, title=expName)
    if dlgc.OK == False:
        core.quit()  # user pressed cancel
    
    
    # Ask for demographic info    
    expInfo = {'participant': '', 'gender': ['Male', 'Female', 'Non-Binary/Other'], 'age': [], 'session': '001'}
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    expInfo['date'] = data.getDateStr()  # add a simple timestamp
    expInfo['expName'] = expName
    expInfo['psychopyVersion'] = psychopyVersion
    
    ##############################################################
    # Set up data folders and filenames
    data_dir = os.path.join(_thisDir, 'data')
    fn = f"{expInfo['participant']}_{expName}_{expInfo['date']}" # file name suffix
    filename = os.path.join(data_dir, fn)
    
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)
        
    if not os.path.isdir(os.path.join(data_dir, 'log')):
        os.mkdir(os.path.join(data_dir, 'log'))

    # Set up ExperimentHandler
    thisExp = data.ExperimentHandler(name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath=_thisDir,
        savePickle=True, saveWideText=True,
        dataFileName=filename)
    
    # save a log file for detail verbose info
    logFile = logging.LogFile(os.path.join(data_dir, 'log', f'{fn}.log'), level=logging.EXP)
    logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

    frameTolerance = 0.001  # how close to onset before 'same' frame

    #########################################################################
    # Setup the Window
    win = visual.Window(
        size=exp.screen_res, fullscr=exp.fullscreen, screen=0, 
        winType='pyglet', allowGUI=False, allowStencil=False,
        monitor=exp.monitor, color=exp.background_color, colorSpace='rgb',
        blendMode='avg', useFBO=True, 
        units='deg')
    win.mouseVisible = False
    win.recordFrameIntervals = True
    win.refreshThreshold = 1/exp.refresh_rate + frameTolerance
    ########################################################################
    
    # Measure the frame rate of the monitor and raise error if it does not match the prespecified refresh rate
    expInfo['frameRate'] = win.getActualFrameRate()
    if expInfo['frameRate'] != None and round(expInfo['frameRate']) == exp.refresh_rate:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        # frameDur = 1.0 / 60.0  # could not measure, so guess
        raise Exception(
            f"frame rate is {expInfo['frameRate']} but you want it to be {exp.refresh_rate}.")
    
    # Setup ioHub
    ioConfig = {}

    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')

    ioSession = '1'
    if 'session' in expInfo:
        ioSession = str(expInfo['session'])
    
    ioServer = io.launchHubServer(window=win, **ioConfig)

    # create a default keyboard (e.g. to check for escape)
    defaultKeyboard = keyboard.Keyboard(backend='iohub')

    # Initialize components for Routine "trial"
    movie_recorded = False
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
            
    ####################### TRIAL HANDLING ####################
    exp.initTrials(win) # initialize the trial structure
    trials = data.TrialHandler(nReps=1.0, method='sequential',
                               extraInfo=expInfo, originPath=-1,
                               trialList=exp.trial_sequence,
                               seed=None, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment

    ################### LOOP STARTS HERE ###########################
    for thisTrial in trials: 
        
        # ------Prepare to start Routine "trial"-------
        continueRoutine = True

        for frame in range(thisTrial.total_frames):
            keys = event.getKeys()
            if len(keys) > 0:
                if 'escape' in keys: # Press ESC 2 times to abort the expeirment
                    if endExpNow:
                        continueRoutine = False
                    else:
                        endExpNow = True
                else:
                    pass
            
            thisTrial.drawTrial(exp, win, frame=frame, keys=keys, trials=trials)
            
            if thisTrial.record:
                win.getMovieFrame()
                movie_recorded = True
            
            # check if all components have finished
            if not continueRoutine or thisTrial.skip:  # a component has requested a forced-end of Routine
                thisTrial.skip = False
                break
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
            
        thisExp.nextEntry()
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break

    # Flip one final time so any remaining win.callOnFlip() 
    # and win.timeOnFlip() tasks get executed before quitting
    win.flip()
    
    # Save movie if recorded any
    if movie_recorded:
        win.saveMovieFrames(f'{fn}.mp4', fps=60)
        
    # Save frame intervals
    win.saveFrameIntervals(fileName=os.path.join(
        data_dir, 'log', f'{fn}_frameIntervals.log'), clear=True)
    print('Overall, %i frames were dropped.' % win.nDroppedFrames)

    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename+'.csv', delim='auto')
    logging.flush()
    # make sure everything is closed down
        
    thisExp.abort()  # or data files will save again on exit
    win.close()
    core.quit()

if __name__ == "__main__":
    runExperiment()