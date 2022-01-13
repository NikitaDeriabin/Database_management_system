from Windows.BaseRowDialog import BaseRowDialog
from Controller.DataBaseController import DataBaseController
from tkinter import messagebox as mb


class AddRowDialog(BaseRowDialog):
    def __init__(self, root, db_connection, table):
        super().__init__(root, db_connection, table)

    def submit(self):
        try:
            row = self.get_data_from_widgets()
            DataBaseController.insert_row(self.db_connection, self.table, row)

            self.destroy()
        except TypeError as type_error:
            mb.showerror("Error", type_error)

