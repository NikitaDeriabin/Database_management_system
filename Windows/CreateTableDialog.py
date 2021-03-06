import tkinter as tk
from tkinter import ttk
from DataBase.DataTypes import DataType
from DataBase.Table import Table
from DataBase.Attribute import Attribute
import constants as const
from tkinter import messagebox as mb


class CreateTableDialog(tk.Toplevel):
    def __init__(self, root, db_connection):
        super().__init__(root)
        self.root = root
        self.db_connection = db_connection
        self.cursor = db_connection.cursor()
        self.widgets = []
        self.frames = []
        self.init_child()

    def init_child(self):
        self.title("Creating table")
        frame = tk.LabelFrame(self, text="Table name", padx=30, pady=10)
        frame.pack(padx=10, pady=5)

        self.entry_table_name = tk.Entry(frame, width=20)
        self.entry_table_name.pack()

        frame_attr = tk.LabelFrame(self, text="Attribute name and type", padx=50, pady=10)
        self.frames.append(frame_attr)
        frame_attr.pack(padx=10, pady=5)

        entry_attr_name = tk.Entry(frame_attr, width=20)
        entry_attr_name.pack(side=tk.LEFT, padx=10)

        box_attr_type = ttk.Combobox(frame_attr, values=DataType.type_list, width=10)
        box_attr_type.current(1)
        box_attr_type.pack(side=tk.RIGHT)

        self.widgets.append((entry_attr_name, box_attr_type))

        frame_btn = tk.Frame(self, height=10)
        frame_btn.pack(side=tk.BOTTOM)

        btn_cancel = tk.Button(frame_btn, text="Cancel", width=20, command=self.cancel)
        btn_cancel.pack(side=tk.LEFT)

        btn_add_attr = tk.Button(frame_btn, text="Add attr", width=20, command=self.add_attribute)
        btn_add_attr.pack(side=tk.LEFT)

        btn_submit = tk.Button(frame_btn, text="Submit", width=20, command=self.submit)
        btn_submit.pack(side=tk.RIGHT)

        self.grab_set()
        self.focus_set()

    def submit(self):
        def check_for_same_attr(attrs):
            attrs_set = set([i.name for i in attrs])
            return len(attrs_set) == len(attrs)

        try:
            table = Table(self.entry_table_name.get())
            attr_str = " (id integer primary key, "
            for widget in self.widgets:
                if len(widget[0].get()) == 0:
                    continue
                attr = Attribute(widget[0].get().replace(' ', ''), widget[1].get().replace(' ', ''), table.name.replace(' ', ''))
                table.add_attribute(attr)
                attr_str += attr.name + " " + "TEXT, "

            attr_str = attr_str[:-2] + ");"
            if len(table.attributes) == 0:
                raise Exception("At least one attribute must be created and filled!")

            if not check_for_same_attr(table.attributes):
                raise Exception("There are common fields!")

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS """ + table.name.replace(' ', '') + attr_str)

            # insert data to attribute table
            for attr in table.attributes:
                self.cursor.execute("""INSERT INTO """ + const.attr_table + " (" + \
                              const.attr_table_name + ", " + const.attr_table_column_name + ", " + \
                              const.attr_table_type + ")" + " VALUES (?, ?, ?)",
                                    (attr.table_name, attr.name, attr.type))

            self.db_connection.commit()
            self.destroy()

        except Exception as ex:
            mb.showerror("Error", ex)

    def cancel(self):
        self.destroy()

    def add_attribute(self):
        frame = tk.LabelFrame(self, text="Attribute name and type", padx=50, pady=10)
        self.frames.append(frame)
        frame.pack(padx=10, pady=5)

        entry_attr_name = tk.Entry(frame, width=20)
        entry_attr_name.pack(side=tk.LEFT, padx=10)

        box_attr_type = ttk.Combobox(frame, values=DataType.type_list, width=10)
        box_attr_type.current(1)
        box_attr_type.pack(side=tk.RIGHT)

        self.widgets.append((entry_attr_name, box_attr_type))
