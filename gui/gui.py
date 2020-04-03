import tkinter as tk

import pages as pg
import page_utils as pu
#
# Main app
#
class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        mainframe = tk.Frame(self)
        mainframe.pack(side="top", fill="both", expand=True)
        mainframe.grid_rowconfigure(0, weight=1)
        mainframe.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for _page in (pg.HomePage, pg.SimPage, pg.AnalysisPage, pg.BodiesPage):
            page_name = _page.__name__
            page = _page(parent=mainframe, controller=self)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="NESW")

        self.show_page("HomePage")

    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()


if __name__=="__main__":
    app = MainApp()
    app.mainloop()
