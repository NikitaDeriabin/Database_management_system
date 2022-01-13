from Windows.BaseRowDialog import BaseRowDialog
from Controller.DataBaseController import DataBaseController
from tkinter import messagebox as mb


class ChangeRowDialog(BaseRowDialog):
    def __init__(self, root, db_connection, table, row_id):
        super().__init__(root, db_connection, table)
        self.row_id = row_id
        self.fill_widgets()

    def fill_widgets(self):
        request_str = """SELECT * FROM """ + self.table.name + " WHERE id=?"
        self.cursor.execute(request_str, (self.row_id,))
        row = self.cursor.fetchone()

        for i in range(len(self.widgets)):
            self.widgets[i][0].delete('0', 'end')
            self.widgets[i][0]['fg'] = 'black'
            self.widgets[i][0].insert(0, row[i + 1])

    def submit(self):
        try:
            row = self.get_data_from_widgets()
            DataBaseController.update_row(db_connection=self.db_connection,
                                          table=self.table, row=row, row_id=self.row_id)
            self.destroy()
        except TypeError as type_error:
            mb.showerror("Error", type_error)