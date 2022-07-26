from psychopy import visual
from trial import Trial
import time

class Outro(Trial):
    def __init__(self, exp, win):
        super(Outro, self).__init__(exp, win)
        self.trl_type = "Outro"
        # Arbitrary number of frames to make the for loop continue until keypress
        self.total_frames = 500000
        self.skip = False  # skip to the next trial?

    def initStim(self, win):
        self.stim = []
        self.breaktext = visual.TextStim(
            win, text=f'The experiment is over.\nThanks for your participation!', color=[-1, -1, -1], colorSpace='rgb', pos=(0, 0))

        self.stim.append(self.breaktext)
    
    def writeData(self, trials):
        trials.addData('TrialType', self.trl_type)
        trials.addData('ExpDur', self.expDur)
    
    def draw(self, exp, win, frame=0, keys=[], trials=None, **kwargs):
        for stim in self.stim:
            stim.draw()

        tEnded = time.time()
        self.expDur = tEnded - exp.tStarted
        
        if len(keys) > 0 or exp.autopilot:
            self.skip = True