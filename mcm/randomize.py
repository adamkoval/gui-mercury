import numpy as np
import sys
import os
import re
import argparse
import importlib

import func as fn

parser = argparse.ArgumentParser()
parser.add_argument('--process_no', '-pno',
                    dest='process_no',
                    action='store')
parser.add_argument('--iter_no', '-k',
                    dest='k',
                    action='store')
parser.add_argument('--bodytype', '-btype',
                    dest='btype',
                    action='store')
args = parser.parse_args()

pno = args.process_no
k = int(args.k)
btype = args.btype
Mjup = 1.898e27 # kg
Msol = 1.989e30 # kg

# Creating an input file
bodyin = open("mercury_{}/{}.in".format(pno, btype), 'w')

# Finding all body files
body_files = [file for file in os.listdir("../gui/setup/") if file.startswith(btype) and file.endswith(".vals")]

for file in body_files:
    st = open("../gui/setup/{}".format(file), "r")
    st = st.readlines()
    for line in st:
        exec(line)

    if btype == "small":
        if file == body_files[0]:
            bodyin.write('\n'.join([
                ")O+_06 Small-body initial data  (WARNING: Do not delete this line!!)",
                ") Lines beginning with `)' are ignored.",
                ")---------------------------------------------------------------------",
                " style (Cartesian, Asteroidal, Cometary) = {}".format(coordinates),
                ")---------------------------------------------------------------------\n"]))
        else:
            pass
        bodyin.write('\n'.join([
            " {:12}ep={}  m={}  r={}  d={}  a1={}  a2={}  a3={}".format(file[:-5], ep, m, r, d, a1, a2, a3),
            "  {}  {}  {}".format(c1, c2, c3),
            "  {}  {}  {}".format(c4, c5, c6),
            "  {}  {}  {}\n".format(Lx, Ly, Lz)]))

    elif btype == "big":
        if file == body_files[0]:
            bodyin.write('\n'.join([
                ")O+_06 Big-body initial data  (WARNING: Do not delete this line!!)",
                ") Lines beginning with `)' are ignored.",
                ")---------------------------------------------------------------------",
                " style (Cartesian, Asteroidal, Cometary) = {}".format(coordinates),
                " epoch (in days) = {}".format(ep),
                ")---------------------------------------------------------------------\n"]))
        else:
            pass
        bodyin.write('\n'.join([
            " {:12}m={}  r={}  d={}  a1={}  a2={}  a3={}".format(file[:-5], m, r, d, a1, a2, a3),
            "  {}  {}  {}".format(c1, c2, c3),
            "  {}  {}  {}".format(c4, c5, c6),
            "  {}  {}  {}\n".format(Lx, Ly, Lz)]))

bodyin.close()
