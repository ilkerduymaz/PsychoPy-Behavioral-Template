# Quick Reference - Module Usage

## Installation

```bash
# From the repository directory
pip install -e .
```

## Import Styles

### Recommended (New Module Style)
```python
from psychopy_template import Experiment, Trial, TrialSequence
from psychopy_template import Fixation, Intro, Outro
from psychopy_template import ResponseScreen, RatingScreen
```

### Also Works (Original Style)
```python
from psychopy_template.experiment import Experiment
from psychopy_template.trial import Trial
from psychopy_template.trialsequence import TrialSequence
```

## Quick Start Example

```python
#!/usr/bin/env python3
from psychopy_template import Experiment, Trial

class MyExperiment(Experiment):
    """Your custom experiment"""
    
    def initDefaults(self, root_dir):
        super().initDefaults(root_dir)
        self.expName = "My Experiment"
        self.total_blocks = 3
        self.cond_per_block = 5
        self.screen_res = (1920, 1080)
        self.fullscreen = True

class MyTrial(Trial):
    """Your custom trial"""
    
    def __init__(self, exp, win):
        super().__init__(exp, win)
        self.trial_duration = 2.0
        # Add your stimuli here

if __name__ == "__main__":
    import os
    exp = MyExperiment(os.getcwd())
    # Run your experiment
```

## Available Components

| Component | Purpose |
|-----------|---------|
| `Experiment` | Base experiment class with configuration |
| `Trial` | Base trial class |
| `TrialGroup` | Group multiple trials together |
| `TrialSequence` | Manage trial sequences and blocks |
| `Fixation` | Display fixation cross |
| `Intro` | Introduction screen |
| `Outro` | Conclusion screen |
| `ResponseScreen` | Collect participant responses |
| `RatingScreen` | Collect ratings (e.g., Likert scales) |
| `Feedback` | Display feedback |
| `BlockBreak` | Break between blocks |
| `TrialBreak` | Break between trials |
| `SampleTrial` | Example trial implementation |
| `MonitorTools` | Monitor configuration utilities |

## Common Patterns

### Subclassing Experiment
```python
from psychopy_template import Experiment

class MyExp(Experiment):
    def initDefaults(self, root_dir):
        super().initDefaults(root_dir)
        # Your configuration
```

### Creating Custom Trials
```python
from psychopy_template import Trial
from psychopy import visual

class MyTrial(Trial):
    def __init__(self, exp, win):
        super().__init__(exp, win)
        self.initStim(win)
    
    def initStim(self, win):
        self.text = visual.TextStim(win, text="Hello")
        self.stim.append(self.text)
```

### Building Trial Sequences
```python
from psychopy_template import TrialSequence, TrialGroup

class MySequence(TrialSequence):
    def __init__(self, exp):
        super().__init__(exp)
        # Build your sequence
```

## File Locations

- **Source code**: `psychopy_template/`
- **Examples**: `examples/`
- **Data output**: `data/`
- **Configuration**: `*.ini` files

## Verification

```bash
# Check structure
python verify_structure.py

# Check imports (requires PsychoPy)
python verify_package.py
```

## Running Examples

```bash
# From repository root
python examples/main.py
```

## Package Information

```python
import psychopy_template
print(psychopy_template.__version__)      # Package version
print(psychopy_template.__all__)          # Available components
```

## Package Name

- Install: `pip install psychopy_template`
- Import: `from psychopy_template import Experiment`

## Tips

1. **Always use absolute paths** when working with files
2. **Subclass components** rather than modifying the source
3. **Use configuration files** (`.ini`) for experiment parameters
4. **Check examples/** for usage patterns

## Getting Help

1. Check `INSTALLATION.md` for installation issues
2. Check `README.md` for general usage
3. Check `examples/` for working code
4. Review source code in `src/` for implementation details
