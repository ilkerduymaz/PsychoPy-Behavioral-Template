from psychopy import visual
import time

class Trial:
    def __init__(self, exp, win):
        ### Trial Info ###
        self.trl_type = self.__class__.__name__

        ### Duration ###
        self.trial_duration = 3 # in seconds
        self.total_frames = self.trial_duration * exp.refresh_rate # total number of frames to display the trial for

        ### Utility ###
        self.record = False # record a video of the trial
        self.skip = False # skip trial

        ### Stimulus ###
        self.stim = []

    def initStim(self, win):
        pass

    def updateStim(self, exp, win, frame=0):
        pass

    def handleInputs(self, exp, win, frame=0, keys=[]):
        pass

    def writeData(self, exp, trials):
        trials.addData("Class", self.trl_type)
        trials.addData(f'TrialEnd-{self.trl_type}', exp.clock.getTime())

    def broadcastVariables(self):   
        broadcast = {}
        return broadcast

    def receiveVariables(self, broadcast=None):
        pass

    def reset(self):
        self.skip = False

    def draw(self, exp, win, frame=0, keys=[], trials=None, **kwargs):
        if frame == 0:
            trials.addData(f'TrialStart-{self.trl_type}', exp.clock.getTime())
            trials.addData(f"TrialEnd-{self.trl_type}", "")
            self.reset()

        self.updateStim(exp, win, frame=frame)

        if self.stim:
            for stim in self.stim:
                stim.draw()

    def handleEEGTriggers(self, exp, win, frame=0):
        if not hasattr(exp, 'eeg'):
            return

        if not hasattr(exp, 'send_triggers'):
            return

        if not hasattr(self, 'trigger'):
            return

        if frame == 0:
            exp.eeg.sendTrigger(win, self.trigger)

        if self.skip:
            exp.eeg.sendTrigger(win, 0)

    def drawTrial(self, exp, win, frame=0, keys=[], trials=None, **kwargs):
        self.draw(exp, win, frame=frame, keys=keys, trials=trials, **kwargs)
        self.handleInputs(exp, win, frame=frame, keys=keys)

        if frame == self.total_frames-1 or self.skip:
            self.writeData(exp, trials)
            self.skip = True

        self.handleEEGTriggers(exp, win, frame=frame)
