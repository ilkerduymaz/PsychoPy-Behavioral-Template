from psychopy import visual
from .trial import Trial
import time

class Outro(Trial):
    def __init__(self, exp, win):
        super(Outro, self).__init__(exp, win)
        self.trl_type = "Outro"
        # Arbitrary number of frames to make the for loop continue until keypress
        self.total_frames = -1
        self.skip = False  # skip to the next trial?
        self.text_color = exp.text_color
        
        self.initStim(win)

    def initStim(self, win):
        self.stim = []
        self.breaktext = visual.TextStim(
            win, text=f'The experiment is over.\nThanks for your participation!', color=self.text_color, colorSpace='rgb', pos=(0, 0))

        self.stim.append(self.breaktext)
    
    def writeData(self, exp, trials):
        super().writeData(exp, trials)
        trials.addData('ExpDur', self.expDur)
        
    def handleInputs(self, exp, win, frame=0, keys=[]):
        if len(keys) > 0 or exp.autopilot:
            self.skip = True
    
    def updateStim(self, exp, win, frame=0):
        if frame == 0:
            tEnded = time.time()
            self.expDur = tEnded - exp.tStarted