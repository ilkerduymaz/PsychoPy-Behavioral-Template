from trial import Trial
from psychopy import visual

class RatingScreen(Trial):
    def __init__(self, exp, win, question="SampleQuestion", choices=[]):
        super().__init__(exp, win)
        self.total_frames = 9999999999
        self.trl_type = "RatingScreen"
        
        self.question = question
        self.choices = choices
        
        posy = len(question)/80 - 0.5
        
        self.text = visual.TextStim(win, text=question, pos=(0.0, posy))
        self.slider = visual.RatingScale(win, choices=choices)
        self.stim = [self.text, self.slider]

    def updateStim(self, exp, win, frame=0):
        if frame < 10:
            win.mouseVisible = True
                     
        if not self.slider.noResponse:
            self.answer = self.slider.getRating()
            self.skip = True
            win.mouseVisible = False
    
    def writeData(self, trials):
        trials.addData(self.question, self.answer)
        trials.addData('TrialType', self.trl_type)