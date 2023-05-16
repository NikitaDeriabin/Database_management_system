from Windows.BaseRowDialog import BaseRowDialog
from tkinter import messagebox as mb


class ChangeRowDialog(BaseRowDialog):
    def __init__(self, root, db_controller, table, row_id):
        super().__init__(root, db_controller, table)
        self.row_id = row_id
        row = self.db_controller.get_row_by_id(table.name, row_id)
        self.fill_widgets(row)

    def fill_widgets(self, row):
        for i in range(len(self.widgets)):
            self.widgets[i][0].delete('0', 'end')
            self.widgets[i][0]['fg'] = 'black'
            self.widgets[i][0].insert(0, row[i + 1])

    def submit(self):
        try:
            row = self.get_data_from_widgets()
            self.db_controller.update_row(table=self.table, row=row, row_id=self.row_id)
            self.destroy()

        except TypeError as type_error:
            mb.showerror("Error", str(type_error))