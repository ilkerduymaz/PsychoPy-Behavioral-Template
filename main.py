#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import psychopy
from psychopy import gui, visual, core, data, event, logging, monitors
import os, binascii, subprocess
import psychopy.iohub as io
from psychopy.hardware import keyboard
from src.experiment import Experiment
from src.send_notification import send_notification
import sys


def runExperiment():
    # Ensure that relative paths start from the same directory as this script
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)

    # Initialize Experiment object
    exp = Experiment(_thisDir)
    win = exp.win

    # Setup ioHub
    ioConfig = {}

    # Setup iohub keyboard
    ioConfig["Keyboard"] = dict(use_keymap="psychopy")
    ioServer = io.launchHubServer(window=win, **ioConfig)

    # create a default keyboard (e.g. to check for escape)
    defaultKeyboard = keyboard.Keyboard(backend="iohub")

    # Set priority
    io.devices.Computer.setPriority("high", disable_gc=False)

    # Initialize components for Routine "trial"
    movie_recorded = False
    endExpNow = False  # flag for 'escape' or other condition => quit the exp

    ################### LOOP STARTS HERE ###########################
    for trial_index, thisTrial in enumerate(exp.trialhandler):
        # ------Prepare to start Routine "trial"-------
        continueRoutine = True
        win.mouseVisible = False
        frame = -1

        while True:
            frame += 1

            keys = event.getKeys()
            if len(keys) > 0:
                if "escape" in keys:  # Press ESC 2 times to abort the expeirment
                    if endExpNow:
                        continueRoutine = False
                    else:
                        endExpNow = True
                else:
                    pass

            thisTrial.drawTrial(
                exp, win, frame=frame, keys=keys, trials=exp.trialhandler, dataobj=exp.expData
            )

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

        exp.writeData(exp.trialhandler)  # add custom exp info to the data file
        exp.expData.nextEntry()
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break

    # Flip one final time so any remaining win.callOnFlip()
    # and win.timeOnFlip() tasks get executed before quitting
    win.flip()
    win.close()

    # Save movie if recorded any
    if movie_recorded:
        win.saveMovieFrames(f"{exp.savefilename}.mp4", fps=60)

    # Save data
    exp.saveData()
    logging.flush()

    # Push data to github
    exp.pushRemote()

    # make sure everything is closed down
    exp.expData.abort()  # or data files will save again on exit
    core.quit()

if __name__ == "__main__":
    try:
        runExperiment(sys.argv[1])
    except:
        print("No experiment type argument given. Running with default arguments")
        runExperiment()
