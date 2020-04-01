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

        big_section = pu.GenericCategory(self, "Big bodies")
        n_big = pu.count_bodies("big")
        bigin_editor = pu.BodiesEditor(big_section, btype="big", default=n_big)

        small_section = pu.GenericCategory(self, "Small bodies")
        n_small = pu.count_bodies("small")
        small_editor = pu.BodiesEditor(small_section, btype="small", default=n_small)

        simulation = pu.GenericCategory(self, "Simulation")
        paramin_button = pu.GenericButton(parent=simulation, text="Edit simulation parameters",
                command=lambda: pu.TextEditor(simulation, file="setup/param.in", comment=""))
        cfgin = "setup/cfg.in"
        if os.path.exists(cfgin):
            cfg = pu.read_cfg(cfgin)
            sims_default = cfg['No. sims'][1:-1]
            pnos_default = cfg['No. parallel'][1:-1]
        else:
            sims_default = ""
            pnos_default = ""
        nosims = pu.GenericInput(simulation, label="No. sims", state='normal', default=sims_default)
        pnos = pu.GenericInput(simulation, label="No. parallel", state='normal', default=pnos_default)
        entry_objects = (nosims, pnos)
        nos = {}
        store_button = pu.GenericButton(simulation, text="Save config",
                command=lambda: pu.get_cfgentries(entry_objects, nos))

        data_conversion = pu.GenericCategory(self, "Data conversion")
        paramin_button = pu.GenericButton(data_conversion, text="Edit element.in",
                command=lambda: pu.TextEditor(data_conversion, file="../mcm/converter/element.in", comment=""))
        bigin_button = pu.GenericButton(parent=data_conversion, text="Edit close.in",
                command=lambda: pu.TextEditor(data_conversion, file="../mcm/converter/close.in", comment=""))


class AnalysisPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pu.GenericPage(self, controller, "Analysis")

        data_conversion = pu.GenericCategory(self, "Convert data")
        files_input = pu.GenericInput(data_conversion, label="Filetype,Range", state='normal')
        convert_button = pu.GenericButton(data_conversion, text="Launch conversion",
                command=lambda: pu.convert_files(files=files_input.get_input()))


class SimPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pu.GenericPage(self, controller, "Simulation")

        pre_status_box = pu.StatusBox(self)
        pre_status_box.status_var.set("Ready to run.")
        go_button = pu.GenericButton(self, text="Run",
                command=lambda: pu.run_sims(pre_status_box))

        sim_status_box = pu.StatusBox(self)
        sim_status_box.status_var.set("n_completed = 0")
        check_status_button = pu.GenericButton(self, text="Check status",
                command=lambda: pu.check_sim_status(sim_status_box))


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
