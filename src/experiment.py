from .trialgroup import TrialGroup
from .trialsequence import TrialSequence
from .sampletrial import SampleTrial
from .trialbreak import TrialBreak
from .blockbreak import BlockBreak
from .fixation import Fixation
from .intro import Intro
from .outro import Outro
from .responsescreen import ResponseScreen
from .ratingscreen import RatingScreen
import psychopy
from psychopy import gui, visual, core, data, event, logging, monitors
import psychopy.iohub as io
from psychopy.hardware import keyboard
from psychopy.tools.monitorunittools import deg2pix
from random import shuffle
from itertools import chain
import copy, time, glob, os
import numpy as np
from numpy.random import randint, normal, choice
from PIL import Image, ImageDraw
import re
import cv2
import binascii
import subprocess
import socket
import json


class Experiment:
    """
    Class for defining experiment parameters like conditions, repetitions, and trial durations.
    """
    expName = None  # Name of the experiment as it will appear in the data file
    lab = None  # add the location of the experiment to the data for future reference

    ### Screen ###
    screen_res = (1920, 1080)  # screen resolution
    refresh_rate = 60  # screen refresh rate
    screen_distance_mm = 570  # participant's distance to the screen
    screen_width_mm = 545  # width of the experiment monitor
    monitor = monitors.Monitor(
        "ExpMonitor", width=screen_width_mm, distance=screen_distance_mm
    )  # monitor profile in Monitor Center
    monitor.setSizePix(screen_res)
    fullscreen = True
    background_color = [0.5, 0.5, 0.5]
    text_color = [1, 1, 1]

    # Block parameters
    blocked = True  # True for block design, False for random design
    total_blocks = 3  # number of blocks
    cond_per_block = 2  # number of repetitions for each condition within a block

    ### Misc ###
    autopilot = False
    doPush = True  # push to github

    def __init__(self, root_dir):
        self.loadConfigJson(root_dir)

        if self.expName == None:
            self.expName = os.path.basename(root_dir)

        if self.lab == None:
            self.lab = socket.gethostname()

        ### Utility ###
        self.clock = core.Clock()  # for timing
        self.tStarted = (
            time.time()
        )  # for calculating experiment duration, do not change
        self.current_block = 1  # for counting blocks, do not change

        ##############################################################
        # Ask for demographic info
        self.popUpDlg()

        # Set up data folders and filenames
        self.initPaths(root_dir)

        # Set up ExperimentHandler
        self.initExpData()

        # Set up window
        self.initWindow()

        ####################### TRIAL HANDLING ####################
        self.initTrials(self.win)  # initialize the trial structure
        self.orderDataCols()
    
    def loadConfigJson(self, root_dir):

        if not os.path.exists(os.path.join(root_dir, "config.json")):
            self.exportConfigJson(root_dir)
            return 
        
        # load object's attributes from a json file
        with open(os.path.join(root_dir, "config.json"), "r") as f:
            self.__dict__ = json.load(f)
    
    def exportConfigJson(self, root_dir):
        # export object's attributes to a json file
        with open(os.path.join(root_dir, "config.json"), "w") as f:
            json.dump(vars(self), f, indent=4)

    def popUpDlg(self):
        expInfo = {
            "participant": binascii.b2a_hex(os.urandom(2)).decode("utf-8"),
            "gender": ["Male", "Female", "Non-Binary/Other"],
            "age": [],
        }
        dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title="Experiment")
        if dlg.OK == False:
            core.quit()  # user pressed cancel

        expInfo["date"] = data.getDateStr()  # add a simple timestamp
        expInfo["psychopyVersion"] = psychopy.__version__
        expInfo["psychopyPath"] = psychopy.__file__

        self.expInfo = expInfo

    def initPaths(self, root_dir):
        self.data_dir = os.path.join(root_dir, "data")
        self.backup_dir = os.path.join(root_dir, "backup")
        self.log_dir = os.path.join(self.data_dir, "log")
        self.incomplete_dir = os.path.join(self.data_dir, "incomplete")

        for d in [self.data_dir, self.backup_dir, self.log_dir, self.incomplete_dir]:
            if not os.path.isdir(d):
                os.mkdir(d)

        self.savefilename = f"{self.expInfo['participant']}_{self.expName}_{self.expInfo['date']}"

    def initWindow(self):
        self.win = visual.Window(
            size=self.screen_res,
            fullscr=self.fullscreen,
            screen=0,
            winType="pyglet",
            allowGUI=False,
            allowStencil=True,
            monitor=self.monitor,
            color=self.background_color,
            colorSpace="rgb",
            blendMode="avg",
            useFBO=True,
        )

        self.win.mouseVisible = False
        self.win.recordFrameIntervals = True
        frameTolerance = 0.001  # how close to onset before 'same' frame
        self.win.refreshThreshold = 1 / self.refresh_rate + frameTolerance

        # Measure the frame rate of the monitor
        self.expInfo["frameRate"] = self.win.getActualFrameRate()

    def initExpData(self):
        self.expData = data.ExperimentHandler(
            name=self.expName,
            version="",
            extraInfo=self.expInfo,
            runtimeInfo=None,
            originPath=None,
            savePickle=False,
            saveWideText=True,
            dataFileName=os.path.join(self.data_dir, self.savefilename),
        )

        # save a log file for detail verbose info
        logFile = logging.LogFile(
            os.path.join(self.log_dir, f"{self.savefilename}.log"), level=logging.EXP
        )
        logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

    def defineTrials(self, win):
        self.trials = [
            {"cond_trl": ResponseScreen(self, win), "nreps": self.cond_per_block}
        ]

    def initTrials(self, win):
        self.defineTrials(win)
        self.trial_sequence = TrialSequence(self, win, endsurvey=False).trial_sequence

        self.trialhandler = data.TrialHandler(
            nReps=1.0,
            method="sequential",
            extraInfo=self.expInfo,
            originPath=-1,
            trialList=self.trial_sequence,
            seed=None,
            name="trials",
        )

        self.expData.addLoop(self.trialhandler)

    def pushRemote(self):
        if self.doPush:
            try:
                os.chdir(self.data_dir)
                subprocess.run(["git", "pull", "origin", "main"])
                subprocess.run(["git", "add", "--all"])
                subprocess.run(["git", "commit", "-m", f'{self.expInfo["participant"]}'])
                subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
            except Exception as err:
                subprocess.run("echo could not push files to repo", shell=True, check=True)
                print("could not push files to repo")
                print(err)

    def saveData(self):
        # Save frame intervals
        self.win.saveFrameIntervals(
            fileName=os.path.join(self.log_dir, f"{self.savefilename}_frameIntervals.log"), clear=True
        )

        # Save backup
        self.expData.saveAsWideText(
            os.path.join(self.backup_dir, "lastfile.csv"), delim="auto"
        )

        # Save actual data
        if not self.trialhandler.finished:
            self.savefilename = os.path.join(
                self.incomplete_dir, f"_incomplete_{self.savefilename}"
            )
        self.expData.saveAsWideText(self.savefilename + ".csv", delim="auto")

    def writeData(self, trials):
        trials.addData("BlockN", self.current_block)
        trials.addData("Lab", self.lab)

    def orderDataCols(self):
        # Order data headers
        self.trialhandler.addData("Participant", "")
        self.trialhandler.addData("BlockN", "")
        self.trialhandler.addData("TrialType", "")
        self.trialhandler.addData("ImageID", "")
        self.trialhandler.addData("Scene", "")
        self.trialhandler.addData("TrialStart", "")
        self.trialhandler.addData("TrialEnd", "")
        self.trialhandler.addData("TimeReacted", "")
        self.trialhandler.addData("PressedKey", "")
        self.trialhandler.addData("Answer", "")
        self.trialhandler.addData("BreakTaken", "")
        self.trialhandler.addData("ExpDur", "")
        self.trialhandler.addData("Lab", "")
