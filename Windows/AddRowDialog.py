from Windows.BaseRowDialog import BaseRowDialog
from tkinter import messagebox as mb


class AddRowDialog(BaseRowDialog):
    def __init__(self, root, db_controller, table):
        super().__init__(root, db_controller, table)

    def submit(self):
        try:
            row = self.get_data_from_widgets()
            self.db_controller.insert_row(self.table, row)

            self.destroy()
        except TypeError as type_error:
            mb.showerror("Error", str(type_error))

