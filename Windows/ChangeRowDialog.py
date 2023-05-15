from Windows.BaseRowDialog import BaseRowDialog
from tkinter import messagebox as mb


class ChangeRowDialog(BaseRowDialog):
    def __init__(self, root, db_controller, table, row_id):
        super().__init__(root, db_controller, table)
        self.row_id = row_id
        row = self._get_row_by_id()
        self.fill_widgets(row)

    def fill_widgets(self, row):
        for i in range(len(self.widgets)):
            self.widgets[i][0].delete('0', 'end')
            self.widgets[i][0]['fg'] = 'black'
            self.widgets[i][0].insert(0, row[i + 1])

    def _get_row_by_id(self):
        request_str = """SELECT * FROM """ + self.table.name + " WHERE id=?"
        self.db_controller.cursor.execute(request_str, (self.row_id,))
        return self.db_controller.cursor.fetchone()

    def submit(self):
        try:
            row = self.get_data_from_widgets()
            self.db_controller.update_row(table=self.table, row=row, row_id=self.row_id)
            self.destroy()

        except TypeError as type_error:
            mb.showerror("Error", str(type_error))