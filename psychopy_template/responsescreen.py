from psychopy import visual
from .trial import Trial
import random


class ResponseScreen(Trial):
    def __init__(self, exp, win):
        super().__init__(exp, win)
        self.trl_type = "ResponseScreen"
        self.text_color = exp.text_color
        self.duration = -1  # in seconds
        self.total_frames = int(exp.refresh_rate * self.duration)

        # A dict of possible answers and their corresponding keys
        self.bindings = {"Answer1": "k", "Answer2": "l"}
        self.correct_answer = None
        self.accuracy = None

        self.answer = None
        self.pressedkey = None

        self.initStim(win)

    def setBindings(self, bindings):
        self.bindings = bindings
        text = [f"{key} - {value}" for key, value in self.bindings.items()]
        self.text.text = "\n".join(text)

    def initStim(self, win):
        text = [f"{key} - {value}" for key, value in self.bindings.items()]
        text = "\n".join(text)
        self.text = visual.TextStim(
            win, text=text.title(), color=self.text_color, colorSpace="rgb", pos=(0, 0)
        )

        self.stim.append(self.text)

    def reset(self):
        super().reset()
        self.accuracy = None
        self.answer = None
        self.pressedkey = None
        self.reaction_time = None

    def handleInputs(self, exp, win, frame=0, keys=[]):
        if exp.autopilot:
            keys.append(random.choice(list(self.bindings.values())))

        if len(keys) == 1:
            if keys[0] in self.bindings.values():
                self.skip = True
                self.answer = [
                    key for key, value in self.bindings.items() if value in keys
                ][0]
                self.pressedkey = keys[0]
                self.reaction_time = frame / exp.refresh_rate

                if self.answer == self.correct_answer:
                    self.accuracy = 1
                else:
                    self.accuracy = 0

    def writeData(self, exp, trials):
        super().writeData(exp, trials)
        trials.addData("Answer", self.answer)
        trials.addData("PressedKey", self.pressedkey)
        trials.addData("TimeReacted", self.reaction_time)
        trials.addData("Accuracy", self.accuracy)

    def receiveVariables(self, broadcast=None):
        if broadcast and "CorrectAnswer" in broadcast:
            self.correct_answer = broadcast["CorrectAnswer"]

    def broadcastVariables(self):
        broadcast = {"Accuracy": self.accuracy}
        return broadcast
