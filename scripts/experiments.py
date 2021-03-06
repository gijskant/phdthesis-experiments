#! /usr/bin/env python
# :noTabs=true:
# (c) Copyright (c) 2017  Gijs Kant
# (c) This file is distributed under the MIT License,
# (c) see the file LICENSE.
"""
experiments.py

Brief: Prepares and runs experiments based on json experiments file.

Author: Gijs Kant <gijskant@protonmail.com>

"""
import os
import sys
import json
from tools import *


"""
Generate files required for the experiments.
"""
def prepare_experiments(config, experiments):
    tools = ToolRegistry(config).tools
    for experiment in experiments:
        experiment_type = experiment['type']
        if (experiment_type == 'pbes'):
            mcrl2 = tools['mcrl2']
            mcrl2.prepare(experiment)
        else:
            print >> sys.stderr, 'Type not supported:', experiment_type

"""
List the experiments.
"""
def list_experiments(config, experiments):
    tools = ToolRegistry(config).tools
    ltsmin = tools['ltsmin']
    ltsmin.print_list(experiments)

"""
Run the experiments.
"""
def run_experiment(config, experiments, index):
    tools = ToolRegistry(config).tools
    ltsmin = tools['ltsmin']
    ltsmin.run(experiments, index)

"""
Analyse the results.
"""
def analyse_results(config, experiments):
    tools = ToolRegistry(config).tools
    ltsmin = tools['ltsmin']
    ltsmin.analyse(experiments)

"""
Read experiment data from a JSON file.
"""
def read_experiments(json_filename):
    json_file = open(json_filename, 'r')
    experiments = json.load(json_file)['data']
    json_file.close()
    return experiments

def read_config(json_filename):
    json_file = open(json_filename, 'r')
    config = json.load(json_file)
    json_file.close()
    return config


def usage():
    command = os.path.basename(sys.argv[0])
    return """Usage: {0} <config.json> <experiments.json> <prepare|list|run|analyse> [index]
For the command 'run', the [index] option is required.""".format(command)


def main():
    if len(sys.argv) <= 3:
        print >> sys.stderr, usage()
        sys.exit(1)

    print >> sys.stderr, os.path.basename(sys.argv[0])
    config_filename = sys.argv[1]
    expriments_filename = sys.argv[2]
    action = sys.argv[3]

    print >> sys.stderr, 'Config file:  ', config_filename
    config = read_config(config_filename)

    print >> sys.stderr, 'Experiments file:  ', expriments_filename
    experiments = read_experiments(expriments_filename)
    print >> sys.stderr, 'Experiments:', len(experiments)

    print >> sys.stderr, 'Action:     ', action
    if action == 'run':
        if len(sys.argv) <= 4:
            print >> sys.stderr, usage()
            sys.exit(1)
        index = int(sys.argv[4])
        run_experiment(config, experiments, index)
    elif action == 'list':
        list_experiments(config, experiments)
    elif action == 'prepare':
        prepare_experiments(config, experiments)
    elif action == 'analyse':
        analyse_results(config, experiments)
    else:
        print >> sys.stderr, usage()
        sys.exit(1)

    print >> sys.stderr, ''
    print >> sys.stderr, 'Done.'


if __name__ == '__main__':
    main()

