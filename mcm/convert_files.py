import os
import argparse
import pandas
import sys
import shutil
import re
from subprocess import Popen

import func as mcfn

pyenv, bashenv, mercuryOG_path, rslts_path = mcfn.read_envfile("envfile.txt")

if rslts_path.endswith("/"):
    rslts_path = rslts_path[:-1]
if mercuryOG_path.endswith("/"):
    mercuryOG_path = mercuryOG_path[:-1]

parser = argparse.ArgumentParser()
parser.add_argument('--files', '-f',
                    dest='files',
                    action='store')
args = parser.parse_args()

options = args.files
ftype, rang = options.split(",")
outputs = os.listdir("{}/outputs/".format(rslts_path))
outputs = mcfn.sort(outputs, ftype, rang)
destination = "{}/converted_outputs".format(rslts_path)
if not os.path.exists(destination):
    os.mkdir(destination)

for outfile in outputs:
    shutil.copyfile("{}/outputs/{}".format(rslts_path, outfile), "converter/{}".format(outfile[-6:]))
    ftype = outfile[-6:-4]
    k = outfile[:-7]
    if ftype == "xv":
        os.system("(cd converter/; ./element6)")
        ext = ".aei"
    elif ftype == "ce":
        os.system("(cd converter/; ./close6)")
        ext = ".clo"
    convfiles = [file for file in os.listdir("converter/") if file.endswith(ext)]
    [shutil.copyfile("converter/{}".format(file), "{}/{}-{}".format(destination, k, file)) for file in convfiles]
    [os.remove("converter/{}".format(file)) for file in convfiles]
    os.remove("converter/{}.out".format(ftype))
