from psychopy import visual
from trial import Trial

class ResponseScreen(Trial):
    def __init__(self, exp, win):
        super().__init__(exp, win)
        self.trl_type = "ResponseScreen"
        
        # A dict of possible answers and their corresponding keys
        self.bindings = { 
                         'a': 'a', 
                         'b': 'b', 
                         'c': 'c', 
                         'd': 'd'
                         }
        
        self.initStim(win)
        
    def initStim(self, win):
        text = [f"{key} - {value}" for key, value in self.bindings.items()]
        text = '\n'.join(text)
        self.text = visual.TextStim(
            win, text=text, color='black', colorSpace='rgb', pos=(0, 0))

        self.stim.append(self.text)

    def handleInputs(self, exp, win, frame=0, keys=[]):
        if len(keys) == 1:
            if keys[0] in self.bindings.values():
                self.skip = True
                self.answer = [key for key, value in self.bindings.items() if value in keys][0]
                self.pressedkey = keys[0]

    
    def writeData(self, trials):
        trials.addData('TrialType', self.trl_type)
        trials.addData('Answer', self.answer)
        trials.addData('PressedKey', self.pressedkey)