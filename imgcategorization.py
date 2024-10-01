from trial import Trial
import random
from psychopy import visual

class ImgCategorization(Trial):
    def __init__(self, exp, win, image=None, category=None):
        super().__init__(exp, win)
        self.trl_type = "ImgCategorization"
        self.category = category

        self.fixation_frames = 2
        self.stim_frames = 3
        self.mask_frames = 10
        self.total_frames = (
            self.mask_frames * 2 + self.stim_frames + self.fixation_frames
        )

        self.mask_contrast = 1
        self.img_path = image

    def initStim(self, exp, win):
        self.image = visual.ImageStim(
            win=win, image=self.img_path, units="deg", size=exp.img_size
        )

        self.masks = random.sample(exp.mondrians, 2)
        self.masks = [visual.ImageStim(
            win=win,
            image=x["mask"],
            units="deg",
            size=exp.img_size,
            contrast=self.mask_contrast,
        ) for x in self.masks]

        self.fixation = visual.TextStim(win=win, text="", color=exp.text_color, pos=(0, 0))

        self.stims = [self.fixation, self.masks[0], self.image, self.masks[1]]
        self.all_frames = ( # display order. 0: fixation, 1: mask, 2: image, 3: mask
            [0] * self.fixation_frames + [1] * self.mask_frames + [2] * self.stim_frames + [3] * self.mask_frames
        )

    def updateStim(self, exp, win, frame=0):
        if frame == 0:
            self.initStim(exp, win)
            win.mouseVisible = False

        self.stim = [self.stims[self.all_frames[frame]]]

    def broadcastVariables(self):
        broadcast = {"CorrectAnswer": self.category}
        return broadcast

    def writeData(self, exp, trials):
        super().writeData(exp, trials)
        trials.addData("ImageID", self.img_path)
        trials.addData("Scene", self.category)
        exp.completed_trials += 1
