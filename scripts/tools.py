#! /usr/bin/env python
# :noTabs=true:
# (c) Copyright (c) 2017  Gijs Kant
# (c) This file is distributed under the MIT License,
# (c) see the file LICENSE.
"""
tools.py

Brief: Utility classes for tools used in the experiments.

Author: Gijs Kant <gijskant@protonmail.com>

"""
import os
import shutil
import re
import subprocess
import sys
import tempfile
import time
import traceback
from humanfriendly import AutomaticSpinner, Spinner, Timer

"""
Runs a command in a shell and returns the stdout.
"""
def run_command(label, command, logfile = None):
    print >> sys.stderr, '-', command
    with AutomaticSpinner(label) as spinner:
        start =  time.time()
        task = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdoutdata, stderrdata) = task.communicate()
        result = task.wait()
        if not result == 0:
            raise Exception('Command failed.')
        if not logfile is None:
            f = open(logfile, 'a')
            f.write(command)
            f.write('\n')
            if not stderrdata is None:
                f.write(stderrdata)
            f.close()
        end = time.time()
    print >> sys.stderr, '  ({:.2f} seconds)'.format((end - start))
    return

"""
Runs a command in a shell and returns the stdout.
"""
def run_simple_command(command):
    task = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    data = task.stdout.read()
    result = task.wait()
    return data

"""
Runs a command in a shell and returns the stdout.
"""
def run_boolean_command(command):
    task = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    result = task.wait()
    return result

"""
Gets the filename without extension.
"""
def get_model_name(filename):
    return os.path.splitext(os.path.basename(filename))[0]


def create_tempfile(filename, suffix):
    modelname = get_model_name(filename)
    (f, filename) = tempfile.mkstemp(suffix, modelname + '.')
    return filename

def get_path_from_config(config, tool):
    c = config.get('tools')
    if c is None:
        return None
    t = c.get(tool)
    if t is None:
        return None
    return t.get('path')

class Tool:
    def prepare(self, data):
        pass

    def run(self, data):
        pass


class Mcrl2(Tool):

    path = ""

    def __init__(self, config):
        path = get_path_from_config(config, 'mcrl2')
        if path is None:
            self.path = self.find_path()
        else:
            self.path = os.path.abspath(path)
        self.path += '/'
        print >> sys.stderr, 'mcrl2 path:', self.path
        test_program = self.path + 'mcrl22lps'
        if not os.path.isfile(test_program):
            raise Exception('mcrl22lps not found.')

    def find_path(self):
        path = run_simple_command('which mcrl22lps')
        mcrl2_dir = os.path.dirname(os.path.abspath(path))
        print >> sys.stderr, 'Found mcrl2 binary in path: ', path,
        return mcrl2_dir

    def check_pbes(self, pbes_filename):
        command = self.path + 'pbesinfo {pbes_filename}'.format(pbes_filename = pbes_filename)
        result = run_boolean_command(command)
        return result == 0

    def generate_pbes(self, data):
        pbes_filename = data['pbes_filename']
        lps_filename = data['lps_filename']
        input_mcf = data['input_mcf']
        preparation_options = data['preparation_options']
        lps2pbes_options = preparation_options['lps2pbes']

        # lps2pbes
        command = self.path + 'lps2pbes -v {lps2pbes_options} -f {input_mcf} {lps_filename} {pbes_filename}'.format(
            lps2pbes_options = lps2pbes_options,
            input_mcf = input_mcf,
            lps_filename = lps_filename,
            pbes_filename = pbes_filename
        )
        # redirect log messages
        logfile = '{pbes_filename}.lps2pbes.log'.format(pbes_filename = pbes_filename)
        try:
            print >> sys.stderr, ''
            start = time.time()

            run_command('Generating ' + pbes_filename, command, logfile)

            end = time.time()
            print >> sys.stderr, 'Generating {} took {:.2f} seconds.'.format(pbes_filename, (end - start))
        except Exception as e:
            print >> sys.stderr, 'Error:', e
            os.remove(pbes_filename)
            sys.exit(1)

    def check_lps(self, lps_filename):
        command = self.path + 'lpsinfo {lps_filename}'.format(lps_filename = lps_filename)
        result = run_boolean_command(command)
        return result == 0

    def generate_lps(self, data):
        lps_filename = data['lps_filename']
        input_mcrl2 = data['input_mcrl2']
        preparation_options = data['preparation_options']
        lin_options = preparation_options['linearisation']
        parunfold_steps = preparation_options['lpsparunfold']

        # redirect log messages
        logfile = '{lps_filename}.log'.format(lps_filename = lps_filename)

        lps_in = ""
        lps_out = ""

        try:
            print >> sys.stderr, ''
            start = time.time()

            # linearisation
            lps_out = create_tempfile(lps_filename, '.lps')
            command = self.path + 'mcrl22lps -v {lin_options} {input_mcrl2} {lps_out}'.format(
                lin_options = lin_options,
                input_mcrl2 = input_mcrl2,
                lps_out = lps_out
            )
            run_command('Linearising ' + input_mcrl2, command, logfile)

            # lpssuminst
            lps_in = lps_out
            lps_out = create_tempfile(lps_filename, '.lps')
            command = self.path + 'lpssuminst {lps_in} {lps_out}'.format(lps_in = lps_in, lps_out = lps_out)
            run_command('lpssuminst ' + input_mcrl2, command, logfile)
            os.remove(lps_in)

            # parunfold
            for step in parunfold_steps:
                lps_in = lps_out
                lps_out = create_tempfile(lps_filename, '.lps')
                command = self.path + 'lpsparunfold -v {options} {lps_in} {lps_out}'.format(
                    options = step,
                    lps_in = lps_in,
                    lps_out = lps_out
                )
                data = run_command('lpsparunfold ' + input_mcrl2, command, logfile)
                os.remove(lps_in)

            # rewrite
            lps_in = lps_out
            lps_out = create_tempfile(lps_filename, '.lps')
            command = self.path + 'lpsrewr -v {lps_in} {lps_out}'.format(lps_in = lps_in, lps_out = lps_out)
            run_command('lpsrewr ' + input_mcrl2, command, logfile)
            os.remove(lps_in)

            # constelm
            lps_in = lps_out
            lps_out = create_tempfile(lps_filename, '.lps')
            command = self.path + 'lpsconstelm -v -c {lps_in} {lps_out}'.format(lps_in = lps_in, lps_out = lps_out)
            run_command('lpsconstelm ' + input_mcrl2, command, logfile)
            os.remove(lps_in)

            # move output to lps_filename
            shutil.move(lps_out, lps_filename)

            end = time.time()
            print >> sys.stderr, 'Generating {} took {:.2f} seconds.'.format(lps_filename, (end - start))
        except Exception as e:
            print >> sys.stderr, 'Error:', e
            traceback.print_exc(file=sys.stderr)
            if os.path.isfile(lps_in):
                os.remove(lps_in)
            if os.path.isfile(lps_out):
                os.remove(lps_out)
            sys.exit(1)

    def prepare(self, data):
        experiment_type = data['type']
        assert experiment_type in ['lps', 'pbes']

        # check if an invalid LPS exists
        lps_filename = data['lps_filename']
        if os.path.isfile(lps_filename):
            if not self.check_lps(lps_filename):
                print >> sys.stderr, 'Found invalid LPS:', lps_filename
                os.remove(lps_filename)

        # generate lps if not exists
        if not os.path.isfile(lps_filename):
            self.generate_lps(data)
        else:
            print >> sys.stderr, 'Existing LPS found:', lps_filename
        if not os.path.isfile(lps_filename):
            raise Exception('Error creating LPS: ' + lps_filename)

        if not experiment_type == 'pbes':
            return

        # check if an invalid PBES exists
        pbes_filename = data['pbes_filename']
        if os.path.isfile(pbes_filename):
            if not self.check_pbes(pbes_filename):
                print >> sys.stderr, 'Found invalid PBES:', pbes_filename
                os.remove(pbes_filename)

        # generate pbes if not exists
        if not os.path.isfile(pbes_filename):
            self.generate_pbes(data)
        else:
            print >> sys.stderr, 'Existing PBES found:', pbes_filename
        if not os.path.isfile(pbes_filename):
            raise Exception('Error creating PBES: ' + pbes_filename)


class Ltsmin(Tool):
    def __init__(self, config):
        path = get_path_from_config(config, 'ltsmin')
        if path is None:
            self.path = self.find_path()
        else:
            self.path = os.path.abspath(path)
        self.path += '/'
        print >> sys.stderr, 'ltsmin path:', self.path
        test_program = self.path + 'pbes2lts-sym'
        if not os.path.isfile(test_program):
            raise Exception('pbes2lts-sym not found.')


    def find_path(self):
        path = run_simple_command('which pbes2lts-sym')
        ltsmin_dir = os.path.dirname(os.path.abspath(path))
        print >> sys.stderr, 'Found ltsmin binary in path:', path,
        return ltsmin_dir


class ToolRegistry:

    tools = {}

    def __init__(self, config):
        self.tools = {
            'mcrl2': Mcrl2(config),
            'ltsmin': Ltsmin(config)
        }

