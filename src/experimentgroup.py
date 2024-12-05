class ExperimentGroup:
    def __init__(self, exp_list=[]):
        self.exp_list = exp_list
        self.mergeTrials()

    def mergeTrials(self):
        self.trial_sequence = []
        self.exp_idx = []
        for i, exp in enumerate(self.exp_list):
            if i == 0:
                exclude = ["Outro", "EndSurvey"]
            if i == len(self.exp_list) - 1:
                exclude = ["Intro"]
            else:
                exclude = ["Intro", "Outro", "EndSurvey"]

            addtrl = [
                trl
                for trl in exp.trial_sequence
                if trl.__class__.__name__ not in exclude
            ]
            self.trial_sequence.extend(addtrl)
            self.exp_idx.extend([i] * len(addtrl))

