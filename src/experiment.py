from .trialgroup import TrialGroup
from .sampletrial import SampleTrial
from .trialbreak import TrialBreak
from .blockbreak import BlockBreak
from .fixation import Fixation
from .intro import Intro
from .outro import Outro
from .responsescreen import ResponseScreen
from .ratingscreen import RatingScreen
from psychopy import monitors, core
from psychopy.tools.monitorunittools import deg2pix
from random import shuffle
from itertools import chain
import copy, time, glob, os
import numpy as np
from numpy.random import randint, normal, choice
from PIL import Image, ImageDraw
import re
import cv2


class Experiment:
    """
    Class for defining experiment parameters like conditions, repetitions, and trial durations.
    """

    def __init__(self):
        ### Screen ###
        self.screen_res = (1920, 1080)  # screen resolution
        self.refresh_rate = 60  # screen refresh rate
        self.screen_distance_mm = 570  # participant's distance to the screen
        self.screen_width_mm = 545  # width of the experiment monitor
        self.monitor = monitors.Monitor(
            "ExpMonitor", width=self.screen_width_mm, distance=self.screen_distance_mm
        )  # monitor profile in Monitor Center
        self.monitor.setSizePix(self.screen_res)
        self.fullscreen = True
        self.background_color = [0.5, 0.5, 0.5]
        self.text_color = [1, 1, 1]

        # Block parameters
        self.total_blocks = 3  # number of blocks
        self.cond_per_block = 2  # number of repetitions for each condition within a block

        ### Debugging Options ###
        self.autopilot = False
        self.distributed_ver = False  # Experiment will be run on different computers?

        ### Utility ###
        self.clock = core.Clock()  # for timing
        self.tStarted = (
            time.time()
        )  # for calculating experiment duration, do not change
        self.current_block = 1  # for counting blocks, do not change
        self.expName = "PsychoPyEEGTemplate"  # Name of the experiment as it will appear in the data file
        self.lab = "lab name/location"  # add the location of the experiment to the data for future reference
        self.doPush = True  # push to github

    def defineTrials(self, win):
        self.trials = [
            {"cond_trl": ResponseScreen(self, win), "nreps": self.cond_per_block}
        ]
    
    def addBeforeTrials(self, win):
        self.fixation = Fixation(self, win, duration=1)
        self.before_trials = [self.fixation]
    
    def addAfterTrials(self, win):
        self.trial_break = TrialBreak(self, win)
        self.after_trials = [self.trial_break]

    def addEndSurvey(self, win):
        self.endsurvey = [
            RatingScreen(
                self,
                win,
                question="Were the instructions you received before the experiment clear? How well do you think you understood the task in the experiment?",
                choices=map(str, range(1, 6)),
            ),
            RatingScreen(
                self,
                win,
                question="How confident were you about the responses you have given during the experiment?",
                choices=map(str, range(1, 6)),
            ),
        ]
    def defineBlock(self, win):
        block = []
        for cond in self.trials:

            trial_group = [self.before_trials, 
                           [cond["cond_trl"]], 
                           self.after_trials]
            
            trial_group = list(chain(*trial_group))

            cond_group = [
                TrialGroup(trial_group=copy.copy(trial_group))
                for _ in range(cond["nreps"])
            ]

            block.extend(cond_group)
        
        return block

    def initTrials(self, win):
        self.addBeforeTrials(win)
        self.addAfterTrials(win)
        self.defineTrials(win)
        self.addEndSurvey(win)

        # Define blocks
        block = self.defineBlock(win)

        trial_sequence = []
        blockbreak = BlockBreak(self, win)
        intro = Intro(self, win)
        trial_sequence.append(intro)
        for ind in range(self.total_blocks):
            thisBlock = copy.copy(block)
            shuffle(thisBlock)
            # trial_sequence.extend(list(chain(*thisBlock)))
            trial_sequence.extend(thisBlock)
            if ind < self.total_blocks - 1:
                trial_sequence.append(blockbreak)

        trial_sequence.extend(self.endsurvey)

        outro = Outro(self, win)
        trial_sequence.append(outro)
        self.trial_sequence = trial_sequence

    def writeData(self, trials):
        trials.addData("BlockN", self.current_block)
        trials.addData("Lab", self.lab)