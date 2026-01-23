"""
PsychoPy Behavioral Template - A modular framework for creating behavioral experiments
"""

__version__ = "0.1.0"

# Import main classes for easy access
from .experiment import Experiment
from .trial import Trial
from .trialgroup import TrialGroup
from .trialsequence import TrialSequence
from .blockbreak import BlockBreak
from .fixation import Fixation
from .intro import Intro
from .outro import Outro
from .responsescreen import ResponseScreen
from .trialbreak import TrialBreak
from .ratingscreen import RatingScreen
from .feedback import Feedback
from .sampletrial import SampleTrial
from .monitortools import MonitorTools

# Define public API
__all__ = [
    "Experiment",
    "Trial",
    "TrialGroup",
    "TrialSequence",
    "BlockBreak",
    "Fixation",
    "Intro",
    "Outro",
    "ResponseScreen",
    "TrialBreak",
    "RatingScreen",
    "Feedback",
    "SampleTrial",
    "MonitorTools",
]
