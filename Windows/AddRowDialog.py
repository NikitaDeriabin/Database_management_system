from Windows.BaseRowDialog import BaseRowDialog
from Controller.DatabaseController import DatabaseController
from tkinter import messagebox as mb


class AddRowDialog(BaseRowDialog):
    def __init__(self, root, db_connection, table):
        super().__init__(root, db_connection, table)

    def submit(self):
        try:
            row = self.get_data_from_widgets()
            DatabaseController.insert_row(self.db_connection, self.table, row)

            self.destroy()
        except TypeError as type_error:
            mb.showerror("Error", str(type_error))

