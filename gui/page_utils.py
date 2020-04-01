import os
import sys
import shutil
import tkinter as tk
from subprocess import Popen

sys.path.append("../")
import mcm.func as mcfn

# Some global definitions
pyenv, bashenv, mercuryOG_path, rslts_path = mcfn.read_envfile("../mcm/envfile.txt")

"""
EVERY PAGE
"""
class GenericPage(tk.Frame):
    def __init__(self, parent, controller, page_name):
        all_buttons = {"Home": 'HomePage',
                "Setup": 'SetupPage',
                "Simulation": 'SimPage',
                "Analysis": 'AnalysisPage'}
        buttons = {key: all_buttons[key] for key in all_buttons if key != page_name}
        tk.Frame.__init__(self, parent)
        label = tk.Label(parent, text=page_name,
                font=("calibri", 15))
        label.pack()
        navbar = NavBar(parent, controller, buttons)


class GenericButton(tk.Button):
    def __init__(self, parent, text, command):
        tk.Button.__init__(self, parent, text=text, command=command)
        self.pack()


class NavButton(tk.Frame):
    def __init__(self, parent, controller, text, dest, col):
        tk.Frame.__init__(self, parent)

        button = tk.Button(parent, text=text,
                command=lambda: controller.show_page(dest))
        button.grid(row=0, column=col)


class NavBar(tk.Frame):
    def __init__(self, parent, controller, buttons):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        for i, text in enumerate(buttons):
            dest = buttons[text]
            NavButton(self, controller, text, dest, i)
        self.pack(side="bottom")


class GenericInput(tk.Frame):
    def __init__(self, parent, label, state):
        tk.Frame.__init__(self, parent)

        self.state = state
        self.label = tk.Label(self, text=label)
        self.label.pack(side="left")
        self.field = tk.Entry(self, state=self.state)
        self.field.pack(side="right")
        self.pack()

    def get_input(self):
        value = self.field.get()
        return value


"""
SETUP PAGE
"""
class BodiesEditor(tk.Frame):
    def __init__(self, parent, btype):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.btype = btype
        self.files = [file for file in os.listdir("setup") if file.endswith(".vals") and file.startswith(self.btype)]
        self.N_bodies = GenericInput(parent, "N bodies", state='normal')
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


class TextWindow(tk.Frame):
    def __init__(self, parent, file):
        tk.Frame.__init__(self, parent)
        self.file = file
        self.parent = parent

        text = open(self.file, 'r').read()
        textbox = tk.Text(parent)
        textbox.pack(side="left")
        textbox.insert(1.0, text)

        scrollbar = tk.Scrollbar(parent, orient="vertical", command=textbox.yview)
        scrollbar.pack(side="right", expand=True, fill='y')


    def save_file(self):
        text = self.textbox.get(1.0, tk.END)
        f = open(self.file, 'w')
        f.write(text)
        f.close()
        self.parent.destroy()


class NoSetupPopup(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)

        label = tk.Label(self, text="No previous setup detected.\nPlease go to the 'Setup' page.")
        label.pack()
        button = tk.Button(self, text="OK",
                command=self.destroy)
        button.pack()


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


def get_entries(entry_objects, dct):
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
    global pyenv
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
    cmd_str = []
    for pno in range(1, n_parallel+1):
        if not pno == n_parallel:
            n_sims = n_per_pno
        else:
            n_sims = N_sims - n_cumu
        cmd_str.append("{} ../mcm/0main.py -no {} -pno {} & ".format(pyenv, n_sims, pno))
        n_cumu += n_per_pno
    cmd_str = "".join(cmd_str)
    os.system(cmd_str)
    os.chdir("../gui/")


"""
ANALYSIS PAGE
"""
def convert_files(files):
    global pyenv
    os.chdir("../mcm/")
    os.system("{} ../mcm/convert_files.py -f {}".format(pyenv, files))
    os.chdir("../gui/")
