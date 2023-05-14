import tkinter as tk
from DataBase.Row import Row
from DataBase.Cell import Cell
from abc import ABC, abstractmethod


class BaseRowDialog(tk.Toplevel, ABC):
    def __init__(self, root, db_connection, table):
        super().__init__(root)
        self.root = root
        self.table = table
        self.db_connection = db_connection
        self.cursor = db_connection.cursor()
        self.widgets = []
        self.frames = []
        self.init_child()

    def init_child(self):
        self.init_widgets()
        self._add_dialog_elements()
        self.grab_set()
        self.focus_set()

    def _add_dialog_elements(self):
        self.frame_btn = tk.Frame(self, height=10, pady=15)
        self.frame_btn.pack(side=tk.BOTTOM)
        self.btn_cancel = tk.Button(self.frame_btn, text="Cancel", width=20, command=self.cancel)
        self.btn_cancel.pack(side=tk.LEFT, padx=10)
        self.btn_submit = tk.Button(self.frame_btn, text="Submit", width=20, command=self.submit)
        self.btn_submit.pack(side=tk.RIGHT)

    def init_widgets(self):
        for attr in self.table.attributes:
            frame = tk.LabelFrame(self, padx=50, pady=10)
            self.frames.append(frame)
            frame.pack(padx=10, pady=5)

            label = tk.Label(frame, text=attr.name)
            label.pack(side=tk.LEFT)
            entry_cell_val = EntryWithPlaceholder(frame, placeholder=attr.type)
            entry_cell_val.pack(side=tk.LEFT, padx=10)

            self.widgets.append((entry_cell_val, attr.name, attr.type))

    def cancel(self):
        self.destroy()

    @abstractmethod
    def submit(self):
        pass

    def get_data_from_widgets(self):
        row = Row(amount_of_attr=len(self.table.attributes))
        cell_list = []
        for widget in self.widgets:
            cell = Cell(name_attr=widget[1], type_attr=widget[2])
            cell.set_val(widget[0].get())
            cell_list.append(cell)

        row.set_cells(cell_list)
        return row


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def focus_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def focus_out(self, *args):
        if not self.get():
            self.put_placeholder()
