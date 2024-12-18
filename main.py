#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
from src.run import runExperiment
import sys

if __name__ == "__main__":
    try:
        runExperiment(sys.argv[1])
    except:
        print("No experiment type argument given. Running with default arguments")
        runExperiment()
