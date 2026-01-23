from psychopy_template import Experiment, ResponseScreen
from CustomTrialSeq import TrialSequence
from psychopy import data
import socket
import os


class CustomExp(Experiment):

    def __init__(self, root_dir):
        super().__init__(root_dir)

    def initDefaults(self, root_dir):
        self.expName = os.path.basename(
            root_dir
        )  # Name of the experiment as it will appear in the data file
        self.lab = (
            socket.gethostname()
        )  # add the location of the experiment to the data for future reference

        ### Screen ###
        self.screen_res = (1920, 1080)  # screen resolution
        self.force_resolution = (
            False  # force screen resolution by using commandline tools
        )
        self.refresh_rate = 60  # screen refresh rate
        self.force_refresh_rate = (
            False  # force screen refresh rate by using commandline tools
        )
        self.screen_distance_mm = 570  # participant's distance to the screen
        self.screen_width_mm = 545  # width of the experiment monitor
        self.fullscreen = True
        self.background_color = [0.5, 0.5, 0.5]
        self.text_color = [1, 1, 1]

        # Block parameters
        self.blocked = True  # True for block design, False for random design
        self.total_blocks = 3  # number of blocks
        self.cond_per_block = (
            2  # number of repetitions for each condition within a block
        )

        ### Misc ###
        self.autopilot = False
        self.doPush = True  # push to github

    def getDefaultsDict(self):
        defaults = {
            "expName": {
                "value": None,
                "comment": "Name of the experiment as it will appear in the data file",
                "section": "GENERAL",
            },
            "lab": {
                "value": None,
                "comment": "add the location of the experiment to the data for future reference",
                "section": "GENERAL",
            },
            "screen_res": {
                "value": self.screen_res,
                "comment": "screen resolution",
                "section": "SCREEN",
            },
            "force_resolution": {
                "value": self.force_resolution,
                "comment": "force screen resolution by using commandline tools",
                "section": "SCREEN",
            },
            "refresh_rate": {
                "value": self.refresh_rate,
                "comment": "screen refresh rate",
                "section": "SCREEN",
            },
            "force_refresh_rate": {
                "value": self.force_refresh_rate,
                "comment": "force screen refresh rate by using commandline tools",
                "section": "SCREEN",
            },
            "screen_distance_mm": {
                "value": self.screen_distance_mm,
                "comment": "participant's distance to the screen",
                "section": "SCREEN",
            },
            "screen_width_mm": {
                "value": self.screen_width_mm,
                "comment": "width of the experiment monitor",
                "section": "SCREEN",
            },
            "fullscreen": {
                "value": self.fullscreen,
                "comment": "True for fullscreen, False for windowed",
                "section": "SCREEN",
            },
            "background_color": {
                "value": self.background_color,
                "comment": "background color",
                "section": "SCREEN",
            },
            "text_color": {
                "value": self.text_color,
                "comment": "text color",
                "section": "SCREEN",
            },
            "autopilot": {
                "value": self.autopilot,
                "comment": "True for autopilot",
                "section": "MISC",
            },
            "doPush": {
                "value": self.doPush,
                "comment": "push to github",
                "section": "MISC",
            },
            "blocked": {
                "value": self.blocked,
                "comment": "True for block design, False for random design",
                "section": "BLOCKS",
            },
            "total_blocks": {
                "value": self.total_blocks,
                "comment": "number of blocks",
                "section": "BLOCKS",
            },
            "cond_per_block": {
                "value": self.cond_per_block,
                "comment": "number of repetitions for each condition within a block",
                "section": "BLOCKS",
            },
        }
        return defaults

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
