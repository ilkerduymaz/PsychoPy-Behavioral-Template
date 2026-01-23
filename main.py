#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
import os
import sys
from CustomExp import CustomExp
from psychopy_template.runner import runExperiment


if __name__ == "__main__":
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)
    exp = CustomExp(_thisDir)

    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            exp = CustomExp(_thisDir)

    runExperiment(exp=exp, root_dir=_thisDir)
