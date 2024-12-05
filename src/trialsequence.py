from .trialgroup import TrialGroup
from .blockbreak import BlockBreak
from .fixation import Fixation
from .intro import Intro
from .outro import Outro
from .responsescreen import ResponseScreen
from .trialbreak import TrialBreak
from .ratingscreen import RatingScreen

# from itertools import chain
import copy
from random import shuffle

class TrialSequence:
    def __init__(self, exp, win, endsurvey=False):
        self.trial_sequence = []

        self.initTrials(exp, win)

        self.addIntro(win)
        if endsurvey: self.addEndSurvey(win)
        self.addOutro(win)

    def initTrials(self, exp, win):
        # Define blocks
        block = self.defineBlock(win)
        blockbreak = BlockBreak(self, win)

        # self.trial_sequence.append(self.intro)
        if exp.blocked == True: # Block design
            for ind in range(exp.total_blocks):
                thisBlock = copy.copy(block)
                shuffle(thisBlock)
                self.trial_sequence.extend(thisBlock)
                if ind < self.total_blocks - 1:
                    self.trial_sequence.append(blockbreak)

        if exp.blocked == False: # Random design
            ntrl = len(self.trial_sequence)
            for ind in range(ntrl, 0, -1):
                if (ind % (ntrl // exp.total_blocks) == 0 
                    and ind >= ntrl // exp.total_blocks 
                    and ind < ntrl):
                    self.trial_sequence.insert(ind, blockbreak)
        # trial_sequence.extend(self.endsurvey)

        # outro = Outro(self, win)
        # trial_sequence.append(outro)
        # self.trial_sequence = trial_sequence

    def defineBlock(self, win):
        block = []
        before_trials = self.addBeforeTrials(win)
        after_trials = self.addAfterTrials(win)

        for cond in self.trials:
            trial_group = [*before_trials, cond["cond_trl"], *after_trials]
            # trial_group = list(chain(*trial_group))
            cond_group = [
                TrialGroup(trial_group=copy.copy(trial_group))
                for _ in range(cond["nreps"])
            ]

            block.extend(cond_group)

        return block

    def addBeforeTrials(self, win):
        self.fixation = Fixation(self, win, duration=1)
        self.before_trials = [self.fixation]
        return self.before_trials

    def addAfterTrials(self, win):
        self.trial_break = TrialBreak(self, win)
        self.after_trials = [self.trial_break]
        return self.after_trials

    def addEndSurvey(self, win):
        self.endsurvey = [
            RatingScreen(
                self,
                win,
                question="Were the instructions you received before the experiment clear? How well do you think you understood the task in the experiment?",
                choices=map(str, range(1, 6)),
            ),
            RatingScreen(
                self,
                win,
                question="How confident were you about the responses you have given during the experiment?",
                choices=map(str, range(1, 6)),
            ),
        ]

        self.trial_sequence.extend(self.endsurvey)

    def addIntro(self, win):
        self.intro = Intro(self, win)
        self.trial_sequence.insert(0, self.intro)

    def addOutro(self, win):
        self.outro = Outro(self, win)
        self.trial_sequence.append(self.outro)

    def append(self, trialseq):
        if not isinstance(trialseq, TrialSequence):
            raise TypeError("Can only append TrialSequences to TrialSequences.")

        # Remove Outro and EndSurvey from trial_sequence
        trial_sequence1 = [
            trl
            for trl in self.trial_sequence
            if trl.__class__.__name__ not in ["Outro", "EndSurvey"]
            ]
        
        # Remove Intro from trialseq
        intro = [
            trl
            for trl in trialseq.trial_sequence
            if trl.__class__.__name__ == "Intro"
        ][0]

        trial_sequence2 = [
            trl
            for trl in trialseq.trial_sequence
            if trl.__class__.__name__ != "Intro"
        ]

        # Add new intro
        intro.text = "The first part is over.\nThe second part is about to start."
        trial_sequence2.insert(0, intro)

        self.trial_sequence = trial_sequence1 + trial_sequence2
