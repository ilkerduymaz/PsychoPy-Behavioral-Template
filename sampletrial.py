from psychopy import visual
from trial import Trial

class SampleTrial(Trial):
    def __init__(self, exp, win):
        super().__init__(exp, win)
        self.trl_type = "TrialTemplate"
        self.initStim(win)
        
    def initStim(self, win):
        self.cross = visual.TextStim(
            win, text='+', color='red', colorSpace='rgb', pos=(0, 0))
        
        self.text = visual.TextStim(
            win, text=f'This is an example trial.', color='black', colorSpace='rgb', pos=(0, 2))
        
        self.stim.append(self.cross)
        self.stim.append(self.text)

    def updateStim(self, exp, win, frame=0):
        pass
    
    def writeData(self, trials):
        super().writeData(trials)
