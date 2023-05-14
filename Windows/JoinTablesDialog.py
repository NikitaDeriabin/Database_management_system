import tkinter as tk
from tkinter import ttk
from DataBase.Base import Base
from tkinter import messagebox as mb
from Windows.JoinTablesResult import JoinTablesResult


class JoinTablesDialog(tk.Toplevel):
    def __init__(self, root, db_connection, tables):
        super().__init__(root)
        self.root = root
        self.db_connection = db_connection
        self.tables = tables
        self.init_child()

    def init_child(self):
        self._render_dialog()
        self.grab_set()
        self.focus_set()

    def _render_dialog(self):
        frame_frs_tbl = tk.LabelFrame(self, text="First table", padx=30, pady=10)
        frame_frs_tbl.pack(padx=10, pady=5)
        frame_scn_tbl = tk.LabelFrame(self, text="Second table", padx=50, pady=10)
        frame_scn_tbl.pack(padx=10, pady=5)
        frame_attr = tk.LabelFrame(self, text="Common column", padx=50, pady=10)
        frame_attr.pack(padx=10, pady=5)
        self.box_frs_table = ttk.Combobox(frame_frs_tbl, values=self.tables, width=10)
        self.box_frs_table.pack()
        self.box_scn_table = ttk.Combobox(frame_scn_tbl, values=self.tables, width=10)
        self.box_scn_table.pack()
        self.box_attr = ttk.Combobox(frame_attr, width=10)
        self.box_attr.bind("<FocusIn>", self.focus_in)
        self.box_attr.pack()
        frame_btn = tk.Frame(self, height=10, pady=15)
        frame_btn.pack(side=tk.BOTTOM)
        btn_cancel = tk.Button(frame_btn, text="Cancel", width=20, command=self.cancel)
        btn_cancel.pack(side=tk.LEFT, padx=10)
        btn_submit = tk.Button(frame_btn, text="Submit", width=20, command=self.submit)
        btn_submit.pack(side=tk.RIGHT)

    def focus_in(self, *args):
        try:
            if not self.box_frs_table.get() or not self.box_scn_table.get():
                raise Exception("Choose tables!")

            db = Base(self.db_connection)
            self.box_attr['values'] = db.get_common_attrs(self.box_frs_table.get(), self.box_scn_table.get())

        except Exception as e:
            self.box_frs_table.focus_set()
            mb.showerror("Error", str(e))

    def submit(self):
        if not self.box_attr.get():
            mb.showerror("Error", "Choose common column!")
        else:
            JoinTablesResult(self.root, self.db_connection, self.box_frs_table.get(),
                             self.box_scn_table.get(), self.box_attr.get())

    def cancel(self):
        self.destroy()


