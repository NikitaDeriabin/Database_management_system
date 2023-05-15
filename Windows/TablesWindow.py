import tkinter as tk
import constants as const
from Windows.CreateTableDialog import CreateTableDialog
from Windows.TableDataWindow import TableDataWindow
from Windows.JoinTablesDialog import JoinTablesDialog
from Windows.BaseWindow import BaseWindow


class TablesWindow(tk.Toplevel, BaseWindow):
    def __init__(self, root, db_name, db_controller):
        super().__init__(root)
        self.tables = None
        self.table_list_box = None
        self.root = root
        self.db_controller = db_controller
        self.db_name = db_name
        self.init_child()

    def init_child(self):
        self._render_window()
        self.display_tables()
        self.grab_set()
        self.focus_set()

    def _render_window(self):
        self.title("DataBase: " + self.db_name)
        self.geometry('850x650+200+50')
        self.resizable(False, False)
        toolbar = tk.Frame(self, bg=const.toolbar_bg, bd=10)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        btn_create_table = tk.Button(toolbar, text='Create table', command=self.open_create_table_dialog, bd=1,
                                     compound=tk.TOP)
        btn_create_table.grid(row=0, column=0, ipadx=10, padx=10)
        btn_select_table = tk.Button(toolbar, text='Select table', command=self.open_selected_table,
                                     bd=1, compound=tk.TOP)
        btn_select_table.grid(row=0, column=1, ipadx=10, padx=10)
        btn_delete_table = tk.Button(toolbar, text='Delete table', command=self.delete_selected_table,
                                     bd=1, compound=tk.TOP)
        btn_delete_table.grid(row=0, column=2, ipadx=10, padx=10)
        btn_refresh_table = tk.Button(toolbar, text='Refresh', command=self.refresh,
                                      bd=1, compound=tk.TOP)
        btn_refresh_table.grid(row=0, column=3, ipadx=10, padx=10)
        btn_join_tables = tk.Button(toolbar, text='Join tables', command=self.join_tables,
                                    bd=1, compound=tk.TOP)
        btn_join_tables.grid(row=0, column=4, ipadx=10, padx=10)

        scrollbar = tk.Scrollbar(self)
        self.table_list_box = tk.Listbox(self, yscrollcommand=scrollbar.set, height=15, width=103)
        self.table_list_box.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=self.table_list_box.yview)

    def open_create_table_dialog(self):
        CreateTableDialog(self.root, self.db_controller, self.refresh)

    def open_selected_table(self):
        selected = self._get_selected_item()
        TableDataWindow(self.root, selected, self.db_controller)

    def _get_selected_item(self):
        return self.table_list_box.get(self.table_list_box.curselection())

    def delete_selected_table(self):
        selected = self._get_selected_item()
        self.db_controller.cursor.execute("""DROP TABLE IF EXISTS """ + selected)
        self.db_controller.cursor.execute("""DELETE FROM """ + const.attr_table + " WHERE " +
                            const.attr_table_name + " = " + "?" + ";", (selected,))
        self.db_controller.connection.commit()
        self.refresh()

    def refresh(self):
        self.display_tables()

    def display_tables(self):
        self.table_list_box.delete(0, tk.END)
        self.db_controller.cursor.execute("""SELECT * FROM sqlite_master WHERE type='table'""")
        self.tables = self.db_controller.cursor.fetchall()
        for tb in self.tables:
            if tb[1] != const.attr_table:
                self.table_list_box.insert(tk.END, tb[1]) #tb[1] - name of table

    def join_tables(self):
        JoinTablesDialog(self.root, self.db_controller,
                         list(map(lambda x: x[1], filter(lambda x: x[1] != const.attr_table, self.tables))))

