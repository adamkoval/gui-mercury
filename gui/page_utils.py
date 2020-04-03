import os
import re
import sys
import shutil
import time
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from subprocess import Popen

sys.path.append("../")
import mcm.func as mcfn
#
# PAGE UTILITIES
#
"""
EVERY PAGE
"""
class GenericPage(tk.Frame):
    def __init__(self, parent, controller, page_name):
        all_buttons = {"Home": 'HomePage',
                "Setup": 'SetupPage',
                "Simulation": 'SimPage',
                "Analysis": 'AnalysisPage'}
        tk.Frame.__init__(self, parent)
        label = tk.Label(parent, text=page_name,
                font=("calibri", 15))
        label.pack()
        self.navbar = NavBar(parent, controller, all_buttons, page_name)


class NavBar(tk.Frame):
    def __init__(self, parent, controller, buttons, curr_page):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.nav_buttons = []
        for i, text in enumerate(buttons):
            dest = buttons[text]
            if curr_page == text:
                self.nav_buttons.append(NavButton(self, controller, text, dest, i, 'disabled'))
            else:
                self.nav_buttons.append(NavButton(self, controller, text, dest, i, 'active'))
        self.man_button = tk.Button(self, text="mercury6.man",
                command=lambda: ManReader(self))
        self.man_button.grid(row=0, column=i+1)
        self.pack(side="bottom")


class NavButton(tk.Frame):
    def __init__(self, parent, controller, text, dest, col, state):
        tk.Frame.__init__(self, parent)

        self.button = tk.Button(parent, text=text, state=state,
                command=lambda: controller.show_page(dest))
        self.button.grid(row=0, column=col)


class ManReader(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)

        mercuryOG_path = mcfn.read_envfile("../mcm/envfile.txt", "mercury_path")
        man_file = "{}/mercury6.man".format(mercuryOG_path)
        text = open(man_file, 'r').read()

        textbox = tk.Text(self)
        textbox.insert(1.0, text)
        textbox.configure(state='disable')
        textbox.pack(side="left", fill="y")

        scrollbar = tk.Scrollbar(self, orient="vertical",
                command=textbox.yview)
        scrollbar.pack(side="right", fill="y")
        textbox.configure(yscrollcommand=scrollbar.set)


class GenericButton(tk.Button):
    def __init__(self, parent, text, command):
        tk.Button.__init__(self, parent, text=text, command=command)
        self.pack()


class GenericInput(tk.Frame):
    def __init__(self, parent, label, state, **kwargs):
        tk.Frame.__init__(self, parent)

        self.state = state
        self.label = tk.Label(self, text=label)
        self.label.pack(side="left")
        if kwargs:
            tv = tk.StringVar(self, value=kwargs['default'])
        else:
            tv = ""
        self.field = tk.Entry(self, state=self.state, textvariable=tv)
        self.field.pack(side="right")
        self.pack()

    def get_input(self):
        value = self.field.get()
        return value


class GenericCategory(tk.Frame):
    def __init__(self, parent, title):
        tk.Frame.__init__(self, parent, bd=5, relief="sunken")
        label = tk.Label(self, text=title, font=("Courier", 15))
        label.pack()
        self.pack()


"""
SETUP PAGE
"""
class BodiesEditor(tk.Frame):
    def __init__(self, parent, btype, default):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.btype = btype
        self.files = [file for file in os.listdir("setup") if file.endswith(".vals") and file.startswith(self.btype)]
        self.N_bodies = GenericInput(parent, "N bodies", state='normal', default=default)
        self.Generate_button = GenericButton(self.parent, "Generate new bodies",
                command=lambda: self.generate_bodies())
        if len(self.files) == 0:
            self.body_no = GenericInput(self.parent, "Body no.", 'disabled')
        else:
            self.body_no = GenericInput(self.parent, "Body no.", 'normal')

        instructions = """
        Please edit each parameter using either a constant value or a function, which may contain
        the variable 'k', such as 'parameter = k**2 + 1000', or be an independent function such
        as 'parameter = np.random.uniform(0, 360)'.

        COORDINATE SYSTEMS (for coordinates 1-6, from manual):
            Cartesian = for xyz coordinates and velocities. Distances should be
                        in AU and velocities in AU per day (1 day = 86400 seconds).

            Asteroidal = Keplerian orbital elements, in an `asteroidal' format.
                         i.e.  a e I g n M, where
                            a = semi-major axis (in AU)
                            e = eccentricity
                            I = inclination (degrees)
                            g = argument of pericentre (degrees)
                            n = longitude of the ascending node (degrees)
                            M = mean anomaly (degrees)

            Cometary = Keplerian orbital elements in a `cometary' format.
                       i.e.  q e I g n T, where
                            q = pericentre distance (AU)
                            e,I,g,n = as above
                            T = epoch of pericentre (days)
        """

        self.edit_body = GenericButton(parent, "Edit body",
                command=lambda: TextEditor(self, file="setup/{}body{}.vals".format(self.btype, self.body_no.get_input()), comment=instructions))

    def generate_bodies(self):
        if len(self.files) != 0:
            os.system("rm setup/{}*.vals".format(self.btype))
        N = int(self.N_bodies.get_input())
        for n in range(1, N+1):
            f = open("setup/{}body{}.vals".format(self.btype, n), 'w')
            f.write("\n".join(['coordinates = "Asteroidal" #Keep this in quotation marks!',
                "ep = 200000 #Epoch of osculation [days]",
                "m = 1e-3 #Mass [M_sol]",
                "r = 1 #Hill radius [Hill radii]",
                "d = 1 #Density [g/cm^3]",
                "a1 = 0 #User-defined force 1",
                "a2 = 0 #User-defined force 2",
                "a3 = 0 #User-defined force 3",
                "c1 = 0 #coordinate 1",
                "c2 = 0 #coordinate 2",
                "c3 = 0 #coordinate 3",
                "c4 = 0 #coordinate 4",
                "c5 = 0 #coordinate 5",
                "c6 = 0 #coordinate 6",
                "Lx = 0 #Spin-angular momentum (x)",
                "Ly = 0 #Spin-angular momentum (y)",
                "Lz = 0 #Spin-angular momentum (z)"]))
            f.close()

        self.body_no.field.config(state='normal')


class TextEditor(tk.Toplevel):
    def __init__(self, parent, file, comment):
        tk.Toplevel.__init__(self, parent)

        self.parent = parent
        self.file = file
        self.comment = comment

        commentbox = tk.Label(self, text=self.comment)
        commentbox.config(justify='left')
        commentbox.grid(column=0, row=0)

        text = open(file, 'r').read()
        self.textbox = tk.Text(self)
        self.textbox.grid(column=0, row=1, sticky='nsew')
        self.textbox.insert(1.0, text)

        scrollbar = tk.Scrollbar(self, orient="vertical",
                command=self.textbox.yview)
        scrollbar.grid(column=1, row=1, sticky='nsew')
        self.textbox.configure(yscrollcommand=scrollbar.set)

        save_button = tk.Button(self, text="Save changes",
                command=lambda: self.save_file())
        save_button.grid(column=0, columnspan=2, row=2)

    def save_file(self):
        text = self.textbox.get(1.0, tk.END)
        f = open(self.file, 'w')
        f.write(text)
        f.close()
        self.destroy()


def count_bodies(btype):
    n = 0
    if not os.path.exists("setup/"):
        create_setupdir()
    for file in os.listdir("setup/"):
        if file.startswith("{}body".format(btype)):
            n += 1
    return n


def create_setupdir():
    mercuryOG_path = mcfn.read_envfile("../mcm/envfile.txt", "mercury_path")
    if not os.path.exists("setup/"):
        os.mkdir("setup/")
    if not os.path.exists("setup/param.in"):
        shutil.copyfile("{}/param.in".format(mercuryOG_path), "setup/param.in")


"""
SIMULATION PAGE
"""
class StatusBox(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack()

        self.status_var = tk.StringVar(self)
        label = tk.Label(self, textvariable=self.status_var)
        label.pack()


def get_cfgentries(entry_objects, dct):
    f = open("setup/cfg.in", "w")
    for obj in entry_objects:
        dct[obj] = obj.get_input()
        f.write("{}: {}\n".format(obj.label["text"], dct[obj]))
    f.close()
    return dct


def read_cfg(cfgin):
    f = open(cfgin, "r")
    lines = f.readlines()
    dct = {}
    for line in lines:
        var, val = line.split(":")
        dct[var] = val
    return dct


def run_sims(status_box):
    pyenv = mcfn.read_envfile("../mcm/envfile.txt", "pyenv")
    rslts_path = mcfn.read_envfile("../mcm/envfile.txt", "results_path")
    cfg = read_cfg("setup/cfg.in")
    cfg_str = "".join(["{}:{}".format(var, cfg[var]) for var in cfg])
    status_str = """Simulation config:\n
    {}
    Running sims.
    """.format(cfg_str)
    status_box.status_var.set(status_str)

    N_sims = int(cfg["No. sims"])
    n_parallel = int(cfg["No. parallel"])
    n_per_pno = N_sims // n_parallel
    n_cumu = 0

    os.chdir("../mcm/")
    if os.path.exists("status.txt"):
        os.remove("status.txt")
    cmd_str = []
    for pno in range(1, n_parallel+1):
        if not pno == n_parallel:
            n_sims = n_per_pno
        else:
            n_sims = N_sims - n_cumu
        os.system("{} ../mcm/0main.py -no {} -pno {} &".format(pyenv, n_sims, pno))
        time.sleep(2)
        n_cumu += n_per_pno
    os.chdir("../gui/")
    shutil.copyfile("setup/param.in", "{}/param.in".format(rslts_path))


def check_sim_status(status_box):
    f = open("../mcm/status.txt", 'r')
    status_str = f.readlines()
    status_box.status_var.set("n_complete = {}".format(status_str[0]))


"""
ANALYSIS PAGE
"""
def convert_files(files):
    pyenv = mcfn.read_envfile("../mcm/envfile.txt", "pyenv")
    os.chdir("../mcm/")
    if not os.path.exists("converter/"):
        mercuryOG_path = mcfn.read_envfile("envfile.txt", "mercury_path")
        mcfn.create_converter(mercuryOG_path)
    else:
        pass
    os.system("{} ../mcm/convert_files.py -f {}".format(pyenv, files))
    os.chdir("../gui/")


class Plotter(tk.Toplevel):
    def __init__(self, parent, k):
        tk.Toplevel.__init__(self, parent)

        self.k = k
        self.rslts_path = mcfn.read_envfile("../mcm/envfile.txt", "results_path")
        self.conv_out_path = "{}/converted_outputs".format(self.rslts_path)
        self.label_dct = {
                'Time (years)': "Time [years]", 'long': "long_perih [deg]", 'M': "M [deg]",
                'a': "a [AU]", 'e': "e", 'i': "I [deg]", 'peri': "arg_perih [deg]",
                'node': "long_asc [deg]", 'Q': "apo_dist [AU]", 'dens': "density [g/cm^3]",
                'f': "true_anom [deg]", 'oblq': "obliq [deg]", 'r': "r_dist [AU]",
                'spin': "spin_per [days]", 'x': "x_pos [m]", 'y': "y_pos [m]", 'z': "z_pos [m]",
                'vx': "x_vel [m/s]", 'vy': "y_vel [m/s]", 'vz': "z_vel [m/s]"
                }

        bodies = []
        for k in self.k.split(","):
            for body in os.listdir(self.conv_out_path):
                if re.match('({})\-'.format(k), body) and body.endswith(".aei"):
                    bodies.append(body)
        headers = self.read_aei("{}/{}".format(self.conv_out_path, bodies[0]), "headers")
        self.var_bar = VariablesBar(self, headers, bodies)

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.fig_frame = FigureFrame(self, self.fig)

        plot_button = GenericButton(self, text="Plot",
                command=lambda: self.make_plot())

    def make_plot(self):
        del self.ax.lines[:]

        checkstates = self.var_bar.checkstates
        for cat in checkstates:
            dct = checkstates[cat]
            globals()[cat] = [var for var in dct if dct[var].get()==True]

        self.plots = []
        for body in bodies:
            path = "{}/{}".format(self.conv_out_path, body)
            data = self.read_aei(path, "data")
            xdat = data[xvars[0]]
            ydat = data[yvars[0]]
            self.plots.append(self.ax.plot(xdat, ydat, label=body))
        if log:
            self.ax.set_xscale("log")
        self.ax.set_xlabel(self.label_dct[xvars[0]])
        self.ax.set_ylabel(self.label_dct[yvars[0]])
        self.ax.legend()
        plt.show()

        self.fig_frame.canvas.draw()

    def read_aei(self, file, which):
        f = open(file, 'r')
        lines = f.readlines()
        headers = re.split('\s\s+', lines[3])
        headers = headers[1:-1]
        if which=="headers":
            return headers
        elif which=="data":
            dct = {}
            for i, header in enumerate(headers):
                dct[header] = [float(line.split()[i])
                        if not re.match("\*+", line.split()[i])
                        else np.nan for line in lines[4:]]
            return dct


class FigureFrame(tk.Frame):
    def __init__(self, parent, fig):
        tk.Frame.__init__(self, parent)

        self.fig = fig
        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.pack()


class VariablesBar(tk.Frame):
    def __init__(self, parent, headers, bodies):
        tk.Frame.__init__(self, parent)

        self.checkstates = {'bodies': {}, 'xvars': {}, 'yvars': {}, 'log': {}}
        lists = [bodies, headers, headers, ["log"]]

        for i, cat in enumerate(self.checkstates):
            section = tk.Frame(self)
            label = tk.Label(section, text="{} - ".format(cat))
            label.grid(row=0, column=0)
            for j, var in enumerate(lists[i]):
                self.checkstates[cat][var] = tk.BooleanVar(self)
                if not var=='log':
                    text = var
                else:
                    text = ""
                chk = tk.Checkbutton(section, text=text, var=self.checkstates[cat][var])
                if cat == 'bodies':
                    self.checkstates[cat][var].set(True)
                elif cat == 'xvars' and var == 'Time (years)':
                    self.checkstates[cat][var].set(True)
                elif cat == 'yvars' and var == 'a':
                    self.checkstates[cat][var].set(True)
                elif cat == 'log':
                    self.checkstates[cat][var].set(True)
                else:
                    pass
                chk.grid(row=0, column=j+1)
            section.pack()
        self.pack()
