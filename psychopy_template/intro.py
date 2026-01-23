from psychopy import visual
from .trial import Trial
from math import floor

class Intro(Trial):
    def __init__(self, exp, win):
        super(Intro, self).__init__(exp, win)
        self.trl_type = "Intro"
        self.seconds = 3  # Imposed minimum break duration in seconds
        self.break_frames = self.seconds * exp.refresh_rate  # Imposed minimum break duration in frames
        # Arbitrary number of frames to make the for loop continue until keypress
        self.total_frames = -1
        self.skip = False  # skip to the next trial?
        self.text_color = exp.text_color
        self.text = "Hi, the experiment is about to start.\n"

        self.initStim(win)

    def initStim(self, win):
        self.stim = []
        self.breaktext = visual.TextStim(
            win, text=self.text, color=self.text_color, colorSpace='rgb', pos=(0, 0))

        self.stim.append(self.breaktext)

    def updateStim(self, exp, win, frame=0):
        if frame < self.break_frames:
            # Calculate remaining time until the participant can skip
            rem_second = self.seconds - floor(frame/exp.refresh_rate)
            self.breaktext.text = self.text + f'You can continue in {rem_second} seconds.'
        elif frame >= self.break_frames:  # Accept keypresses after the imposed duration
            self.breaktext.text = 'Press any key to continue.'

    def handleInputs(self, exp, win, frame=0, keys=[]):
        if frame >= self.break_frames and (len(keys) > 0 or exp.autopilot):
            self.skip = True
