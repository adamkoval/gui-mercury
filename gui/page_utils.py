import tkinter as tk

#
#   Utilities to be used in pages
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
    def __init__(self, parent, label):
        tk.Frame.__init__(self, parent)

        self.label = tk.Label(self, text=label)
        self.label.pack(side="left")
        self.field = tk.Entry(self)
        self.field.pack(side="right")
        self.pack()

    def get_input(self):
        value = self.field.get()
        return value


"""
SETUP PAGE
"""
class TextEditor(tk.Toplevel):
    def __init__(self, parent, file):
        tk.Toplevel.__init__(self, parent)

        self.file = file
        self.parent = parent
        text = open(file, 'r').read()
        self.textbox = tk.Text(self)
        self.textbox.grid(column=0, row=0, sticky='nsew')
        self.textbox.insert(1.0, text)

        scrollbar = tk.Scrollbar(self, orient="vertical",
                command=self.textbox.yview)
        scrollbar.grid(column=1, row=0, sticky='nsew')
        self.textbox.configure(yscrollcommand=scrollbar.set)

        save_button = tk.Button(self, text="Save changes",
                command=lambda: self.save_file())
        save_button.grid(column=0, columnspan=2, row=1)

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


def get_entries(entry_objects, dct):
    f = open("setup/cfg.in", "w")
    for obj in entry_objects:
        dct[obj] = obj.get_input()
        f.write("{}: {}\n".format(obj.label["text"], dct[obj]))
    f.close()
    return dct


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
    cfg = read_cfg("setup/cfg.in")
    cfg_str = "".join(["{}:{}".format(var, cfg[var]) for var in cfg])
    status_str = """Simulation config:\n
    {}
    Running sims.
    """.format(cfg_str)
    status_box.status_var.set(status_str)

    n_sims = int(cfg["No. sims"])
    n_parallel = int(cfg["No. parallel"])
    no_per_pno = n_sims // n_parallel
    no_cumulative = 0
    for pno in range(1, n_parallel+1):
        if not pno == n_parallel:
            print("python3 0main.py -no {} -pno {}".format(no_per_pno, pno))
        else:
            print("python3 0main.py -no {} -pno {}".format(n_sims - no_cumulative, pno))
        no_cumulative += no_per_pno

"""
ANALYSIS PAGE
"""


