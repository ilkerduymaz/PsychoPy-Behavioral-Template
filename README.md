# PsychoPy-Behavioral-Template

A modular Python package for creating PsychoPy behavioral experiments. This template provides a flexible and extensible framework for building psychology experiments with support for trials, blocks, responses, ratings, and more.

## Features

- 🧩 **Modular Design**: Reusable components for trials, blocks, fixations, responses, and more
- 🎯 **Flexible Trial Sequences**: Support for blocked and randomized designs
- 📊 **Data Management**: Automatic data logging and organization
- 🖥️ **Monitor Configuration**: Tools for managing screen settings and resolutions
- 🎨 **Customizable**: Easy to extend and customize for your specific needs

## Installation

### Install from source (development)

```bash
# Clone the repository
git clone https://github.com/yourusername/psychopy-behavioral-template.git
cd psychopy-behavioral-template

# Install in development mode
pip install -e .
```

### Install as a package

```bash
pip install -e .
```

## Quick Start

### Using as a Module

Once installed, you can import and use the package in your own experiments:

```python
from psychopy_template import Experiment, TrialSequence, Trial

# Create your custom experiment class
class MyExperiment(Experiment):
    def initDefaults(self, root_dir):
        super().initDefaults(root_dir)
        self.expName = "My Custom Experiment"
        # Configure your experiment parameters
        
# Run your experiment
if __name__ == "__main__":
    exp = MyExperiment("/path/to/experiment")
    # Your experiment logic here
```

### Using the Example Scripts

The repository includes example scripts that demonstrate the package usage:

```bash
# Run the example experiment
python examples/main.py
```

## Project Structure

```
psychopy_template/
├── psychopy_template/        # Core package modules
│   ├── __init__.py          # Package initialization
│   ├── experiment.py        # Base Experiment class
│   ├── trial.py             # Trial base class
│   ├── trialsequence.py     # Trial sequence management
│   ├── trialgroup.py        # Trial grouping
│   ├── responsescreen.py    # Response collection
│   ├── ratingscreen.py      # Rating scales
│   ├── fixation.py          # Fixation crosses
│   ├── intro.py             # Introduction screens
│   ├── outro.py             # Outro screens
│   ├── blockbreak.py        # Block breaks
│   ├── trialbreak.py        # Trial breaks
│   ├── feedback.py          # Feedback screens
│   └── monitortools.py      # Monitor configuration
├── examples/                # Example experiment scripts
│   ├── CustomExp.py        # Example custom experiment
│   ├── CustomTrialSeq.py   # Example trial sequence
│   └── main.py             # Example main script
├── data/                    # Data output directory
├── backup/                  # Backup directory
├── pyproject.toml          # Package configuration
├── setup.py                # Setup script
├── MANIFEST.in             # Package manifest
├── LICENSE                 # License file
└── README.md               # This file
```

## Usage Guide

### Creating a Custom Experiment

1. **Subclass the Experiment class**:
```python
from psychopy_template import Experiment

class MyExperiment(Experiment):
    def initDefaults(self, root_dir):
        super().initDefaults(root_dir)
        # Set your parameters
        self.expName = "My Experiment"
        self.total_blocks = 3
        self.cond_per_block = 2
```

2. **Create a custom trial sequence**:
```python
from psychopy_template import TrialSequence, TrialGroup

class MyTrialSequence(TrialSequence):
    def __init__(self, exp):
        super().__init__(exp)
        # Define your trial groups and sequence
```

3. **Run your experiment**:
```python
if __name__ == "__main__":
    exp = MyExperiment("/path/to/experiment")
    # Implement your experiment loop
```

## Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

### Code Formatting

```bash
black src/
```

## Requirements

- Python >= 3.8
- PsychoPy >= 2023.1.0

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Original Template

Template for a PsychoPy experiment. Mainly for self-use, but might be helpful if you are trying to figure out how to create experiments using PsychoPy Coder.
