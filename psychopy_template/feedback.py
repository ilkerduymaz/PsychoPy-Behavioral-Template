from .trial import Trial
from psychopy import visual


class Feedback(Trial):
    #
    # mode can be "fixation" or "text"
    def __init__(self, exp, win, mode="text"):
        super().__init__(exp, win)
        self.trial_duration = 0.5  # in seconds
        self.total_frames = self.trial_duration * exp.refresh_rate
        self.accuracy = None
        self.give_feedback = False
        self.mode = mode
        self.initStim(exp, win)

    def initStim(self, exp, win):
        if self.mode == "fixation":
            text = "+"
        elif self.mode == "text":
            text = "Feedback"
        else:
            raise ValueError("Invalid mode for Feedback trial")

        self.text = visual.TextStim(
            win,
            text=text,
            color=exp.text_color,
            colorSpace="rgb",
            pos=(0, 0),
            height=1,
            units="deg",
        )

    def setText(self):
        if self.accuracy == 1:
            self.text.text = "Correct"
            self.text.color = [-1, 1, -1]
        elif self.accuracy == 0:
            self.text.text = "Incorrect"
            self.text.color = [1, -1, -1]
        else:
            self.text.text = "No response"
            self.text.color = "white"

        if self.mode == "fixation":
            self.text.text = "+"

        self.stim = [self.text]
        self.accuracy = None

    def receiveVariables(self, broadcast=None):
        if not broadcast:
            self.give_feedback = False
            return

        if broadcast and "GiveFeedback" in broadcast:
            self.give_feedback = broadcast["GiveFeedback"]

        if broadcast and "Accuracy" in broadcast:
            self.accuracy = broadcast["Accuracy"]

    def updateStim(self, exp, win, frame=0):
        if not self.give_feedback:
            self.skip = True
            return

        if frame == 0:
            self.setText()

    def drawTrial(self, exp, win, frame=0, keys=..., trials=None, **kwargs):
        super().drawTrial(exp, win, frame, keys, trials, **kwargs)
        if self.skip:
            self.stim = []