##
#
# Function file for simulation package
#
##
import numpy as np
import os
import re
import sys
import shutil

def read_envfile(envfile):
    """
    Reads in envfile to assign local environments of
    python and bash.
    In:
        > envfile - (str) path to envfile.txt
    Out:
        > pyenv, bashenv, mercury_path, results_path -
        (str) paths to python and bash environments +
        results and mercury paths.
    """
    with open(envfile, 'r') as f:
        lines = [line for line in f.readlines() if line[0] is not '#']
        names = []
        for line in lines:
            name = line.split()[0]
            value = line.split()[2]
            globals()[name] = value
            names.append(name)
        return [globals()[name] for name in names]


def disp(res_float, fraction, direction=''):
    """
    For the outer planet, sets initial displacement outside of
    or migration distance inside of the resonance under
    consideration.
    In:
        > res_float - (float) fractional value of resonance
        under consideration, i.e., 2/1=2.0, 5/3=1.66667, and
        so on
        > fraction - (float) fraction of distance
        between neighboring resonances by which to
        displace the outer planet
        > direction - (str) 'in' or 'out', depending on
        whether the user sets the initial displacement or
        the final displacement inside of the resonance
    Out:
        > disp - displacement from resonance in T_i/T_o.
    """
    res_floats = [9/7, 4/3, 7/5, 3/2, 5/3, 2/1, 3/1]
    for i in range(1, len(res_floats)-1):
        if res_floats[i] == res_float:
            if direction == 'out':
                disp = fraction * (res_floats[i+1] - res_floats[i])
            elif direction == 'in':
                disp = fraction * (res_floats[i] - res_floats[i-1])
    return disp


def count_completed(results_path):
    """
    Counts number of files present in the results directory.
    In:
        > results_path - (str) path to results directory
    Out:
        > N_completed - (int) number of completed runs
        present in the directory.
    """
    #print(' ~~~~~~~~~~~~~~~~~~~~~~~~\n',
    #      'func.py/count_completed():\n',
    #      'Checking results directory.\n')
    dirs = ['inputs', 'outputs']
    numbers = {}
    for _dir in dirs:
        numbers[_dir] = len(os.listdir('{}/{}'.format(results_path, _dir)))

    N_completed = int(numbers['inputs'])//3
    return N_completed

    #if numbers['inputs'] == numbers['outputs']:
    #    N_completed = int(numbers['inputs'])//3
    #    return N_completed
    #else:
    #    print(' Please check the numbers of runs in each output directory:\n',
    #          '     N_inputs: {}\n'.format(numbers['inputs']),
    #          '     N_outputs: {}\n'.format(numbers['outputs']),
    #          '~~~~~~~~~~~~~~~~~~~~~~~~\n')
    #    sys.exit()


def make_rsltpath(results_path):
    """
    Create directory into which simulation results are placed.
    """
    def make_if(path):
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            pass

    paths = ["{}".format(results_path),
             "{}/outputs".format(results_path),
             "{}/inputs".format(results_path)]

    for path in paths:
        make_if(path)


class MercuryInstance:
    """
    Offers utilities to create and destroy a mercury instance from
    the compiled git version.
    """
    def __init__(self, pno, mercury_og):
        self.pno = pno
        self.mercury_og = mercury_og

    def create(self):
        os.mkdir("mercury_{}".format(self.pno))
        for file in ["files.in", "mercury6", "message.in"]:
            shutil.copyfile("{}/{}".format(self.mercury_og, file),
                    "mercury_{}/{}".format(self.pno, file))
        os.system("chmod +x mercury_{}/mercury6".format(self.pno))
        shutil.copyfile("../gui/setup/param.in",
                "mercury_{}/param.in".format(self.pno))

    def destroy(self):
        shutil.rmtree("mercury_{}".format(self.pno), ignore_errors=True)


def sort(outputs, ftype, rang):
    # Sort by ftype
    if ftype == "both":
        outputs = [file for file in outputs if file[-6:-4] in ("xv", "ce")]
    elif ftype == "xv":
        outputs = [file for file in outputs if file[-6:-4] == "xv"]
    elif ftype == "ce":
        outputs = [file for file in outputs if file[-6:-4] == "ce"]
    else:
        print(' ~~~~~~~~~~~~~~~~~~~~~~~~\n',
                'func.py/sorter.sortby_body():\n',
                'Please enter either "xv", "ce" or "both".\n')
        return

    # Sort by range
    if rang == "all":
        pass
    elif re.match("[0-9]+\-[0-9]+", rang):
        rang0 = int(rang.split("-")[0])
        rang1 = int(rang.split("-")[1])
        outputs = [file for file in outputs if int(file[:-7]) in range(rang0, rang1)]
    elif re.match("[0-9]+", rang):
        outputs = [file for file in outputs if file[:-7]==rang]
    else:
        print(' ~~~~~~~~~~~~~~~~~~~~~~~~\n',
                'func.py/sorter.sortby_range():\n',
                'Please enter either single number e.g. "599",\n',
                'a range e.g. "32-344" (incl-excl), or "both".\n')
        return

    return outputs
