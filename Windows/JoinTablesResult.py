import tkinter as tk
from tkinter import ttk


from Controller.DataBaseController import DataBaseController
from DataBase.Attribute import Attribute
from DataBase.Base import Base


class JoinTablesResult(tk.Toplevel):
    def __init__(self, root, db_connection, table1, table2, comm_attr):
        super().__init__(root)
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
        table1 = DataBaseController.get_table_data(self.tbl1, self.db_connection)
        table2 = DataBaseController.get_table_data(self.tbl2, self.db_connection)

        columns = [attr.name for attr in table1.attributes]
        print("column before:", columns)
        columns += list(filter(lambda x: x.lower() != self.comm_attr, [attr.name for attr in table2.attributes]))
        print("column after:", columns)
        print()

        self.tree = ttk.Treeview(self, columns=tuple(columns), height=15, show='headings') #show maybe drop

        col_width = 950 // len(tuple(columns))
        for col in enumerate(columns):
            print(col, type(col))
            self.tree.column('#'+str(col[0] + 1), width=col_width, anchor=tk.CENTER)
            self.tree.heading('#'+str(col[0] + 1), text=str(col[1]).lower())

        self.tree.pack()

    def view_records(self):
        [self.tree.delete(i) for i in self.tree.get_children()]

        db = Base(self.db_connection)
        table = db.get_join_table(self.comm_attr, self.tbl1, self.tbl2)
        for row in table.rows:
            self.tree.insert('', 'end', values=tuple(row))