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

        label = tk.Label(self, text="Pre-sim setup",
                font=("Courier", 15))
        label.pack()
        paramin_button = pu.GenericButton(self, text="Edit param.in",
                command=lambda: pu.TextEditor(self, "setup/param.in"))
        bigin_button = pu.GenericButton(parent=self, text="Edit big.in",
                command=lambda: pu.TextEditor(self, "setup/big.in"))
        smallin_button = pu.GenericButton(parent=self, text="Edit small.in",
                command=lambda: pu.TextEditor(self, "setup/small.in"))

        label = tk.Label(self, text="Data conversion",
                font=("Courier", 15))
        label.pack()
        paramin_button = pu.GenericButton(self, text="Edit element.in",
                command=lambda: pu.TextEditor(self, "../mcm/converter/element.in"))
        bigin_button = pu.GenericButton(parent=self, text="Edit close.in",
                command=lambda: pu.TextEditor(self, "../mcm/converter/close.in"))


class AnalysisPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pu.GenericPage(self, controller, "Analysis")


class SimPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pu.GenericPage(self, controller, "Simulation")

        no_sims = pu.GenericInput(self, "No. sims")
        pnos = pu.GenericInput(self, "No. parallel")
        entry_objects = (no_sims, pnos)
        dct = {}
        store_button = pu.GenericButton(self, text="Store",
                command=lambda: pu.get_entries(entry_objects, dct))

        #print_button = pu.GenericButton(self, text="Print",
        #        command=lambda: print(dct))


#    def get_entries(entry_objects):
#        dct = {}
#        for obj in entry_objects:
#            dct[obj] = obj.get_input()
#        return dct


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
