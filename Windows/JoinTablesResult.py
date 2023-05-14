import tkinter as tk
from tkinter import ttk
from Controller.DatabaseController import DatabaseController
from DataBase.Base import Base


class JoinTablesResult(tk.Toplevel):
    def __init__(self, root, db_connection, table1, table2, comm_attr):
        super().__init__(root)
        self.tree = None
        self.db_connection = db_connection
        self.tbl1 = table1
        self.tbl2 = table2
        self.comm_attr = comm_attr
        self.init_child()
        self.view_records()

    def init_child(self):
        self.title("Join tables: " + self.tbl1 + " and " + self.tbl2)
        self.geometry('950x650+200+50')

        self.init_tree()

        self.grab_set()
        self.focus_set()

    def init_tree(self):
        table1 = DatabaseController.get_table_data(self.tbl1, self.db_connection)
        table2 = DatabaseController.get_table_data(self.tbl2, self.db_connection)

        columns = self._get_joined_columns(table1, table2)

        self.tree = ttk.Treeview(self, columns=tuple(columns), height=15, show='headings')
        self._set_columns(columns)
        self.tree.pack()

    def _get_joined_columns(self, table1, table2):
        columns = [attr.name for attr in table1.attributes]
        columns += list(filter(lambda x: x.lower() != self.comm_attr, [attr.name for attr in table2.attributes]))
        return columns

    def _set_columns(self, columns):
        col_width = 950 // len(tuple(columns))
        for col in enumerate(columns):
            temp_col = '#' + str(col[0] + 1)
            self.tree.column(temp_col, width=col_width, anchor=tk.CENTER)
            self.tree.heading(temp_col, text=str(col[1]).lower())

    def view_records(self):
        [self.tree.delete(i) for i in self.tree.get_children()]

        db = Base(self.db_connection)
        table = db.get_join_table(self.comm_attr, self.tbl1, self.tbl2)
        for row in table.rows:
            self.tree.insert('', 'end', values=tuple(row))