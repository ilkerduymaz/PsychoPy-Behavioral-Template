from trial import Trial
from psychopy import visual

class Fixation(Trial):
    def __init__(self, exp, win, duration=1):
        super(Fixation, self).__init__(exp, win)
        
        self.trl_type = "Fixation"
        self.trial_duration = duration # in seconds
        self.total_frames = self.trial_duration * exp.refresh_rate
        self.initStim(win)
        
    def initStim(self, win):
        self.cross = visual.TextStim(
            win, text='+', color='red', colorSpace='rgb', pos=(0, 0))

        self.stim.append(self.cross)