# How to Import After Installing

## Unified Package and Import Names ✓

This package has **unified naming** - the package name and import name match!

After installing this package with:
```bash
pip install -e /path/to/PsychoPy\ Behavioral\ Template
# OR
pip install psychopy_template
```

You import using `psychopy_template`:

```python
# ✓ Correct - unified naming
from psychopy_template import Experiment, Trial, TrialSequence

# ✓ Also works
from psychopy_template.experiment import Experiment
from psychopy_template.trial import Trial
```

### Package Names

- **Package name** (for pip): `psychopy_template`
- **Module name** (for import): `psychopy_template`
- **Note**: Using snake_case everywhere for consistency!

## Complete Example Workflow

### Installing in Another Project

```bash
# In your other project directory
pip install -e /path/to/PsychoPy\ Behavioral\ Template
```

### Using in Your Code

```python
#!/usr/bin/env python3
# my_experiment.py (in your other project)

from psychopy_template import Experiment, Trial, TrialSequence
from psychopy import visual

class MyExperiment(Experiment):
    def initDefaults(self, root_dir):
        super().initDefaults(root_dir)
        self.expName = "My New Experiment"

if __name__ == "__main__":
    import os
    exp = MyExperiment(os.getcwd())
    # Your code here
```

## Quick Reference

| Action | Command/Code |
|--------|--------------|
| Install from local path | `pip install -e /path/to/package` |
| Install from git | `pip install git+https://github.com/user/repo.git` |
| Import | `from psychopy_template import Experiment` |
| Import specific class | `from psychopy_template.experiment import Experiment` |
| Check if installed | `pip show psychopy_template` |
| List installed packages | `pip list \| grep psychopy` |
| Uninstall | `pip uninstall psychopy_template` |

## Testing Your Installation

After installing, test with:

```python
# test_import.py
try:
    from psychopy_template import Experiment
    import psychopy_template
    print("✓ Import successful!")
    print(f"  Version: {psychopy_template.__version__}")
except ImportError as e:
    print(f"✗ Import failed: {e}")
```

## Common Issues

### "No module named 'psychopy_template'"

**Solution:** Make sure you installed the package first:
```bash
pip install -e /path/to/package
```

### "No module named 'psychopy'"

**Solution:** Install PsychoPy:
```bash
pip install psychopy
```

### Imports work in one project but not another

**Solution:** Install the package in each Python environment:
```bash
# Activate your environment first, then
pip install -e /path/to/package
```

## For Development

If you're actively developing both projects:

```bash
# Install in editable mode
pip install -e /path/to/PsychoPy\ Behavioral\ Template

# Changes to the source code are immediately available
# No need to reinstall after each change
```

## Summary

**Unified naming:**
- Package name: `psychopy_template` (for pip install)
- Import name: `psychopy_template` (for Python imports)
- Import with: `from psychopy_template import Experiment`

Snake_case everywhere for perfect consistency!
