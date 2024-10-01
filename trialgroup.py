from trial import Trial
import copy
class TrialGroup(Trial):
    def __init__(self, trial_group=[]):
        self.trl_type = "TrialGroup"
        self.trial_group = [copy.copy(trl) for trl in trial_group]
        self.reset()

    def getAttributes(self):
        self.__dict__.update(self.trial_group[self.trial_index].__dict__)
        self.total_frames = self.total_frames_og

    def reset(self):
        super().reset()
        self.trial_frames = []
        self.total_frames_og = 0
        for trl in self.trial_group:
            self.total_frames_og += trl.total_frames
            self.trial_frames.append(list(range(trl.total_frames)))

        # self.total_frames_og = len(self.trial_frames)
        self.trial_index = 0
        self.finished_frames = 0

        self.getAttributes()
        self.trl_type = "TrialGroup"
        for trl in self.trial_group:
            trl.reset()

    def drawTrial(self, exp, win, frame=0, keys=[], trials=None, dataobj=[], **kwargs):
        if frame == 0:
            self.reset()

        nframe = frame - self.finished_frames

        current_trial = self.trial_group[self.trial_index]
        current_trial.drawTrial(
            exp,
            win,
            frame=self.trial_frames[self.trial_index][nframe],
            keys=keys,
            trials=trials,
            **kwargs
        )
        self.getAttributes()

        if (
            self.trial_frames[self.trial_index][nframe]
            == (current_trial.total_frames - 1)
            or current_trial.skip
        ):
            self.trial_index += 1
            self.finished_frames = frame + 1
            exp.writeData(trials)

            # if self.trial_index < len(self.trial_group):
            #     dataobj.nextEntry()

            broadcasted_vars = current_trial.broadcastVariables()

            if broadcasted_vars:
                for trial in self.trial_group:
                    trial.receiveVariables(broadcasted_vars)

        if self.trial_index == len(self.trial_group):
            self.skip = True
        else:
            self.skip = False  # Prevent individual trials overriding the
            # skip due to getAttributes()
