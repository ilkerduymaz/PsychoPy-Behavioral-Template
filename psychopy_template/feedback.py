from .trial import Trial
from psychopy import visual


class Feedback(Trial):
    def __init__(self, exp, win):
        super().__init__(exp, win)
        self.trial_duration = 0.5  # in seconds
        self.total_frames = self.trial_duration * exp.refresh_rate
        self.accuracy = None
        self.initStim(exp, win)

    def initStim(self, exp, win):
        self.text = visual.TextStim(
            win,
            text="Feedback",
            color=exp.text_color,
            colorSpace="rgb",
            pos=(0, 0),
        )

        self.stim.append(self.text)

    def setText(self):
        if self.accuracy == 1:
            self.text.text = "Correct"
            self.text.color = [0, 1, 0]
        elif self.accuracy == 0:
            self.text.text = "Incorrect"
            self.text.color = [1, 0, 0]
        else:
            self.text.text = "No response"
    
    def receiveVariables(self, broadcast=None):
        if broadcast and "Accuracy" in broadcast:
            self.accuracy = broadcast["Accuracy"]
    
    def updateStim(self, exp, win, frame=0):
        if frame == 0:
            self.setText()