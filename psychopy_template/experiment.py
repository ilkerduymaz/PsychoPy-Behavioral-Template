from .trialsequence import TrialSequence
from .responsescreen import ResponseScreen
import psychopy
from psychopy import gui, visual, core, data, event, logging, monitors
import time 
import os
import binascii
import subprocess
import socket
import json
import configparser
from .monitortools import MonitorTools


class Experiment:
    """
    Class for defining experiment parameters like conditions, repetitions, and trial durations.
    """
    def __init__(self, root_dir):

        self.initDefaults(root_dir)

        #############################################################
        # self.loadConfigJson(root_dir)
        self.loadConfigIni(root_dir)
        #############################################################

        if self.expName == None:
            self.expName = os.path.basename(root_dir)

        if self.lab == None:
            self.lab = socket.gethostname()

        ### Monitor ###
        self.forceMonitorSettings() # depends on self.force_resolution and self.force_refresh
        self.monitor = monitors.Monitor(
            "ExpMonitor", width=self.screen_width_mm, distance=self.screen_distance_mm
        )  # monitor profile in Monitor Center
        self.monitor.setSizePix(self.screen_res) # resolution won't be set correctly without this

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

    def loadConfigJson(self, root_dir):

        if not os.path.exists(os.path.join(root_dir, f"{self.__class__.__name__}_config.json")):
            self.exportConfigJson(root_dir)
            return 

        if not os.path.exists(os.path.join(root_dir, f"{self.__class__.__name__}_config.ini")):
            self.exportConfigIni(root_dir)

        # load object's attributes from a json file
        with open(
            os.path.join(root_dir, f"{self.__class__.__name__}_config.json"), "r"
        ) as f:
            self.__dict__ = json.load(f)

    def exportConfigJson(self, root_dir):
        # export object's attributes to a json file
        with open(
            os.path.join(root_dir, f"{self.__class__.__name__}_config.json"), "w"
        ) as f:
            json.dump(self.__dict__, f, indent=4)

    def loadConfigIni(self, root_dir):
        config = configparser.ConfigParser()
        config.optionxform = str
        filename = os.path.join(root_dir, f"{self.__class__.__name__}_{self.lab}_config.ini")

        if not os.path.exists(filename):
            self.exportConfigIni(root_dir)
            return

        config.read(filename)
        kwargs = {}

        import ast

        def infer_type(value):
            """
            Infer Python types from a string.
            Handles bool, int, float, tuple, list, and str.
            """
            value = value.strip()

            # First, try literal_eval (handles tuples, lists, numbers, booleans)
            try:
                result = ast.literal_eval(value)
                return result
            except (ValueError, SyntaxError):
                pass

            # Fallback to lowercased booleans
            if value.lower() in {'true', 'yes', 'on'}:
                return True
            elif value.lower() in {'false', 'no', 'off'}:
                return False

            return value  # Default: str

        for section in config.sections():
            kwargs = kwargs | dict({k: infer_type(v) for k, v in config[section].items()})

        self.__dict__.update(kwargs)

    def exportConfigIni(self, root_dir):
        config = configparser.ConfigParser(allow_no_value=True)
        config.optionxform = str
        defaults = self.getDefaultsDict()

        for name, value in vars(self).items():
            if name in defaults:
                section = defaults[name]["section"]
                comment = defaults[name]["comment"]
            else:
                section = "DEFAULT"
                comment = None

            if not config.has_section(section):
                config[section] = {}

            if comment is not None:
                config.set(section, f"# {comment}")

            config[section][name] = str(value)

        with open(
            os.path.join(root_dir, f"{self.__class__.__name__}_{self.lab}_config.ini"),
            "w",
        ) as configfile:
            config.write(configfile)

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

    def forceMonitorSettings(self):
        montool = MonitorTools()

        current_res = montool.getResolution()
        current_refresh = montool.getRefreshRate()

        if current_res != self.screen_res and self.force_resolution:
            new_res = self.screen_res
        else:
            new_res = current_res

        if current_refresh != self.refresh_rate and self.force_refresh_rate:
            new_refresh = self.refresh_rate
        else:
            new_refresh = current_refresh

        montool.set_settings(new_res, new_refresh)


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
        self.trialhandler.addData("BlockN", "")
        self.trialhandler.addData("Class", "")
        self.trialhandler.addData("TimeReacted", "")
        self.trialhandler.addData("PressedKey", "")
        self.trialhandler.addData("Answer", "")
        self.trialhandler.addData("BreakTaken", "")
        self.trialhandler.addData("ExpDur", "")
        self.trialhandler.addData("Lab", "")
