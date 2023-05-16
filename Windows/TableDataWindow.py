import tkinter as tk
from tkinter import ttk
import constants as const
from Windows.AddRowDialog import AddRowDialog
from Windows.ChangeRowDialog import ChangeRowDialog
from DataBase.Attribute import Attribute
from Windows.BaseWindow import BaseWindow

class TableDataWindow(tk.Toplevel, BaseWindow):
    def __init__(self, root, table_name, db_controller):
        super().__init__(root)
        self.tree = None
        self.root = root
        self.db_controller = db_controller
        self.table_name = table_name
        self.table = self.db_controller.get_table_data(table_name)
        self.init_child()
        self.display_records()

    def init_child(self):
        self._render_window()
        self.init_tree()
        self.grab_set()
        self.focus_set()

    def _render_window(self):
        self.title("Table: " + self.table_name)
        self.geometry('850x650+200+50')
        self.resizable(False, False)
        toolbar = tk.Frame(self, bg=const.toolbar_bg, bd=10)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        btn_add_row = tk.Button(toolbar, text='Add row', command=self.open_add_row_dialog, bd=1,
                                compound=tk.TOP)
        btn_add_row.grid(row=0, column=0, ipadx=10, padx=10)
        btn_change_row = tk.Button(toolbar, text='Change row', command=self.open_change_row_dialog,
                                   bd=1, compound=tk.TOP)
        btn_change_row.grid(row=0, column=1, ipadx=10, padx=10)
        btn_delete_row = tk.Button(toolbar, text='Delete row', command=self.delete_selected_row,
                                   bd=1, compound=tk.TOP)
        btn_delete_row.grid(row=0, column=2, ipadx=10, padx=10)
        btn_refresh_table = tk.Button(toolbar, text='Refresh', command=self.refresh,
                                      bd=1, compound=tk.TOP)
        btn_refresh_table.grid(row=0, column=3, ipadx=10, padx=10)

    def display_records(self):
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db_controller.get_rows(self.table.name)]

    def open_add_row_dialog(self):
        AddRowDialog(self.root, self.db_controller, self.table)

    def open_change_row_dialog(self):
        row_id = self.tree.set(self.tree.selection()[0], "#1")
        ChangeRowDialog(self.root, self.db_controller, self.table, row_id)

    def delete_selected_row(self):
        selected_row_id = []
        for selected_item in self.tree.selection():
            selected_row_id.append(self.tree.set(selected_item, '#1'))
        self.db_controller.delete_row(self.table, tuple(selected_row_id))

        self.refresh()

    def refresh(self):
        self.display_records()

    def init_tree(self):
        id_attr = Attribute(name="id", data_type="int", table_name=self.table.name)
        columns = [str(id_attr)] + [str(attr.name) for attr in self.table.attributes]
        self.tree = ttk.Treeview(self, columns=tuple(columns), height=15, show='headings')

        self._set_columns(columns)
        self.tree.pack()

    def _set_columns(self, columns):
        col_width = 850 // len(columns)
        for col in columns:
            self.tree.column(col, width=col_width, anchor=tk.CENTER)
            self.tree.heading(col, text=col)