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

        container = tk.Frame(self, bd=5, relief="sunken")
        container.pack()

        welcome = tk.Label(container, text="MERCURY_gui",
                font=("adura", 15))
        welcome.pack()
        blurb = tk.Label(container, text=("Welcome to the MERCURY6 gui.\n"
                + "This gui was created as a university assignment.\n"
                + "It is intended to be used as a quick-start tool\n"
                + "for students working with the MERCURY6 symplectic\n"
                + "integrator."), font=("adura", 13))
        blurb.pack()
        signed = tk.Label(container, text="Written by A. Koval, in the year 2020.")
        signed.pack()


class SetupPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pu.GenericPage(self, controller, "Setup")

        categories = {}
        categories[0] = self.category(self, "Simulation")
        paramin_button = pu.GenericButton(parent=categories[0], text="Simulation parameters",
                command=lambda: pu.TextEditor(categories[0], "setup/param.in"))
        bigin_button = pu.GenericButton(parent=categories[0], text="Big bodies",
                command=lambda: pu.TextEditor(categories[0], "setup/big.in"))
        smallin_button = pu.GenericButton(parent=categories[0], text="Small bodies",
                command=lambda: pu.TextEditor(categories[0], "setup/small.in"))
        nosimss = pu.GenericInput(categories[0], "No. sims")
        pnos = pu.GenericInput(categories[0], "No. parallel")
        entry_objects = (nosimss, pnos)
        nos = {}
        store_button = pu.GenericButton(categories[0], text="Save config",
                command=lambda: pu.get_entries(entry_objects, nos))

        categories[2] = self.category(self, "Data conversion")
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

        status_box = pu.StatusBox(self)
        status_box.status_var.set('Hello')
        go_button = pu.GenericButton(self, text="Run",
                command=lambda: status_box.status_var.set("Running sim."))


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
