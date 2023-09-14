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
        
    def initStim(self, win):
        pass

    def updateStim(self, exp, win, frame=0):
        pass

    def handleInputs(self, exp, win, frame=0, keys=[]):
        pass
    
    def writeData(self, trials):
        pass

    def reset(self):
        self.skip = False
    
    def draw(self, exp, win, frame=0, keys=[], trials=None, **kwargs):
        self.updateStim(exp, win, frame=frame)
        
        if self.stim:
            for stim in self.stim:
                stim.draw()
    
    def drawTrial(self, exp, win, frame=0, keys=[], trials=None, **kwargs):
        self.draw(exp, win, frame=frame, keys=keys, trials=trials)
        self.handleInputs(exp, win, frame=frame, keys=keys)
        
        if frame == self.total_frames-1 or self.skip:
            self.writeData(trials)
