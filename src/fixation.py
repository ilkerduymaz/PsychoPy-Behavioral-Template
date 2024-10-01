from .trial import Trial
from psychopy import visual


class Fixation(Trial):
    def __init__(self, exp, win, duration=1):
        super(Fixation, self).__init__(exp, win)

        self.trl_type = "Fixation"
        self.trial_duration = duration  # in seconds
        self.total_frames = self.trial_duration * exp.refresh_rate
        self.doFeedback = False
        self.initStim(win)

    def initStim(self, win):
        self.cross = visual.TextStim(
            win, text="+", color="red", colorSpace="rgb", pos=(0, 0)
        )

        self.stim.append(self.cross)

    def updateStim(self, exp, win, frame=0):
        if frame == 0 and self.doFeedback:
            if exp.last_resp_accuracy == 1:
                self.cross.color = "green"
            elif exp.last_resp_accuracy == 0:
                self.cross.color = "red"
            else:
                self.cross.color = exp.text_color
        
        if frame == self.total_frames -1:
            exp.last_resp_accuracy = None

    def writeData(self, exp, trials):
        pass
