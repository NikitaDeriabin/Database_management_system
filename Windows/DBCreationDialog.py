import tkinter as tk
from Controller.DataBaseController import DataBaseController


class DBCreationDialog(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.init_child()

    def init_child(self):
        self.title("Creating database")
        self.geometry('400x50+400+300')
        self.resizable(False, False)

        tk.Label(self, text="Name:").grid(row=0, column=0, padx="10", pady="10")
        self.entry_name = tk.Entry(self, width=20)
        self.entry_name.grid(row=0, column=1, padx="10", pady="10")

        btn_submit = tk.Button(self, text='Submit', command=self.submit, bd=1)
        btn_submit.grid(row=0, column=2, padx="10", pady="10")

        btn_cancel = tk.Button(self, text='Cancel', command=self.cancel, bd=1)
        btn_cancel.grid(row=0, column=3, padx="10", pady="10")


        self.grab_set()
        self.focus_set()

    def submit(self):
        DataBaseController.create_db(self.entry_name.get())
        self.destroy()

    def cancel(self):
        self.destroy()