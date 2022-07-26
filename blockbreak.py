from psychopy import visual
from math import floor
from trial import Trial

class BlockBreak(Trial):
    def __init__(self, exp, win):
        super(BlockBreak, self).__init__(exp, win)
        self.trl_type = "BlockBreak"
        self.seconds = 5  # Imposed minimum break duration in seconds
        self.break_frames = self.seconds * exp.refresh_rate  # Imposed minimum break duration in frames
        self.total_frames = 500000 # Arbitrary number of frames to make the for loop continue until keypress
        self.skip = False  # skip to the next trial?
        self.break_taken = 0
        
        self.initStim(win)
        
    def initStim(self, win):
        self.stim = []
        self.breaktext = visual.TextStim(
            win, text=f'You can continue in X seconds.', color=[-1, -1, -1], colorSpace='rgb', pos=(0, 0))

        self.stim.append(self.breaktext)
    
    def updateStim(self, exp, frame=0):
        if frame < self.break_frames:
            # Calculate remaining time until the participant can skip
            rem_second = self.seconds - floor(frame/exp.refresh_rate)
            self.breaktext.text = f'Block: {exp.current_block}/{exp.total_blocks}\nTake a break for at least {self.seconds} seconds.\nYou can continue in {rem_second} seconds.'
        elif frame >= self.break_frames:  # Accept keypresses after the imposed duration
            self.breaktext.text = f'Block: {exp.current_block}/{exp.total_blocks}\nPress any key to continue.'
    
    def writeData(self, trials):
        trials.addData('TrialType', self.trl_type)
        trials.addData('BreakTaken', self.break_taken)
        self.break_taken = 0        

    def draw(self, exp, win, frame=0, keys=[], trials=None, **kwargs):
        self.updateStim(exp, frame=frame)
        
        for stim in self.stim:
            stim.draw()

        if frame > self.break_frames and (len(keys) > 0 or exp.autopilot):
            self.skip = True
            self.break_taken = frame/exp.refresh_rate
            exp.current_block += 1


                