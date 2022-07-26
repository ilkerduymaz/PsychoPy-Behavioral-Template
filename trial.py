from psychopy import visual

class Trial:
    def __init__(self, exp, win):
        ### Trial Info ###
        self.trl_type = "Trial"
        
        ### Duration ###
        self.trial_duration = 3 # in seconds
        self.total_frames = self.trial_duration * exp.refresh_rate # total number of frames to display the trial for
        
        ### Utility ###
        self.record = False # record a video of the trial
        self.skip = False # skip trial
        
        ### Stimulus ###
        self.stim = []
        self.initStim(win)
        
    def initStim(self, win):
        self.cross = visual.TextStim(
            win, text='+', color='red', colorSpace='rgb', pos=(0, 0))
        
        self.text = visual.TextStim(
            win, text=f'This is an example trial.', color='black', colorSpace='rgb', pos=(0, 2))
        
        self.stim.append(self.cross)
        self.stim.append(self.text)

    def updateStim(self, frame=0):
        pass
    
    def writeData(self, trials):
        trials.addData('TrialType', self.trl_type)
    
    def draw(self, exp, win, frame=0, keys=[], trials=None, **kwargs):
        self.updateStim(frame=frame)
        
        for stim in self.stim:
            stim.draw()
    
    def drawTrial(self, exp, win, frame=0, keys=[], trials=None, **kwargs):
        
        self.draw(exp, win, frame=frame, keys=keys, trials=trials)
        
        if frame == self.total_frames-1 or self.skip:
            self.writeData(trials)
