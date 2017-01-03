#! /usr/bin/env python
# :noTabs=true:
# (c) Copyright (c) 2017  Gijs Kant
# (c) This file is distributed under the Apache Software License, Version 2.0
# (c) (https://www.apache.org/licenses/LICENSE-2.0.txt).
"""
experiments.py

Brief: Prepares and runs experiments based on json experiments file.

Author: Gijs Kant <gijskant@protonmail.com>

"""
import os
import sys
import re
import json
import StringIO
from tools import *


"""
Generate files required for the experiments.
"""
def prepare_experiments(experiments):
    tools = ToolRegistry().tools
    for experiment in experiments:
        experiment_type = experiment['type']
        if (experiment_type == 'pbes'):
            mcrl2 = tools['mcrl2']
            mcrl2.prepare(experiment)
        else:
            print >> sys.stderr, 'Type not supported:', experiment_type

"""
Run the experiments.
"""
def run_experiments(experiments):
    pass


"""
Read experiment data from a JSON file.
"""
def read_experiments(json_filename):
    json_file = open(json_filename, 'r')
    experiments = json.load(json_file)['data']
    json_file.close()
    return experiments


def usage():
    command = os.path.basename(sys.argv[0])
    return "Usage: {0} <experiments.json> <prepare|run>".format(command)


def main():
    if len(sys.argv) <= 2:
        print >> sys.stderr, usage()
        sys.exit(1)

    print >> sys.stderr, os.path.basename(sys.argv[0])

    json_filename = sys.argv[1]
    print >> sys.stderr, 'JSON file:  ', json_filename
    experiments = read_experiments(json_filename)
    print >> sys.stderr, 'Experiments:', len(experiments)

    action = sys.argv[2]
    print >> sys.stderr, 'Action:     ', action
    if (action == 'run'):
        run_experiments(experiments)
    elif (action == 'prepare'):
        prepare_experiments(experiments)
    else:
        print >> sys.stderr, usage()
        sys.exit(1)

    print >> sys.stderr, ''
    print >> sys.stderr, 'Done.'


if __name__ == '__main__':
    main()

