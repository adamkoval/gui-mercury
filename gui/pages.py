import tkinter as tk

import os

import page_utils as pu

#
#   Pages
#
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pu.GenericPage(self, controller, "Home")


class SetupPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pu.GenericPage(self, controller, "Setup")

        categories = {}
        categories[0] = self.category(self, "Pre-sim setup")
        paramin_button = pu.GenericButton(parent=categories[0], text="Edit param.in",
                command=lambda: pu.TextEditor(categories[0], "setup/param.in"))
        bigin_button = pu.GenericButton(parent=categories[0], text="Edit big.in",
                command=lambda: pu.TextEditor(categories[0], "setup/big.in"))
        smallin_button = pu.GenericButton(parent=categories[0], text="Edit small.in",
                command=lambda: pu.TextEditor(categories[0], "setup/small.in"))

        categories[1] = self.category(self, "Simulation")
        nosimss = pu.GenericInput(categories[1], "No. sims")
        pnos = pu.GenericInput(categories[1], "No. parallel")
        entry_objects = (nosimss, pnos)
        nos = {}
        store_button = pu.GenericButton(categories[1], text="Save No. sims & no. parallel",
                command=lambda: pu.get_entries(entry_objects, nos))

        categories[2] = self.category(self, "Simulation")
        paramin_button = pu.GenericButton(categories[2], text="Edit element.in",
                command=lambda: pu.TextEditor(categories[2], "../mcm/converter/element.in"))
        bigin_button = pu.GenericButton(parent=categories[2], text="Edit close.in",
                command=lambda: pu.TextEditor(categories[2], "../mcm/converter/close.in"))

        for i in categories:
            categories[i].pack(fill='both')

    def category(self, parent, title):
        category = tk.Frame(self, bd=5, relief="sunken")
        label = tk.Label(category, text=title, font=("Courier", 15))
        label.pack()
        return category


class AnalysisPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pu.GenericPage(self, controller, "Analysis")


class SimPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pu.GenericPage(self, controller, "Simulation")

        go_button = pu.GenericButton(self, text="Run",
                command=lambda: print("Running sims."))
        status_box = pu.StatusBox(self)


class SetupPopup(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)

        setup = self.check_setup()
        label = tk.Label(self, text=self.check_setup())
        label.pack()
        button = tk.Button(self, text="OK",
                command=self.destroy)
        button.pack()

    def check_setup(self):
        setup = os.listdir('setup/')
        if len(setup) == 0:
            return str("No previous setup detected.\n"
                    +"Please go to the 'Setup' page\n"
                    +"and create a new setup.")
        elif 'big.in' not in setup:
            return str("big.in is missing.\n"
                    +"Please provide one or go to\n"
                    +"the 'Setup' page to create a\n"
                    +"new setup.")
        elif 'small.in' not in setup:
            return str("small.in is missing.\n"
                    +"Please provide one or go to\n"
                    +"the 'Setup' page to create a\n"
                    +"new setup.")
        elif 'param.in' not in setup:
            return str("param.in is missing.\n"
                    +"Please provide one or go to\n"
                    +"the 'Setup' page to create a\n"
                    +"new setup.")
        else:
            return str("Old setup found.")
