from trial import Trial
import copy
class TrialGroup(Trial):
    def __init__(self, trial_group=[]):
        self.trial_group = [copy.copy(trl) for trl in trial_group]
        self.reset()
    
    def getAttributes(self):
        self.__dict__.update(self.trial_group[self.trial_index].__dict__)
        self.total_frames = self.total_frames_og
    
    def reset(self):
        super().reset()
        self.total_frames_og = 0
        for trl in self.trial_group:
            self.total_frames_og += trl.total_frames

        self.trial_index = 0
        self.finished_frames = 0

        self.getAttributes()
        
        for trl in self.trial_group:
            trl.reset()
        
    def drawTrial(self, exp, win, frame=0, keys=[], trials=None, **kwargs):
        if frame == 0:
            self.reset()
            
        if self.trial_index < len(self.trial_group):
            if self.trial_group[self.trial_index].total_frames < frame - self.finished_frames or self.trial_group[self.trial_index].skip:
                self.finished_frames += self.trial_group[self.trial_index].total_frames
                # self.trial_group[self.trial_index].reset()
                self.trial_index += 1
                
            self.trial_group[self.trial_index].drawTrial(
                exp, win, frame=frame - self.finished_frames, keys=keys, trials=trials, **kwargs)
            self.getAttributes()
            
        else:
            self.skip = True
