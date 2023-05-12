import tkinter as tk
import constants as const
from Controller.FileReader import FileReader
from Windows.DBCreationDialog import DBCreationDialog
from Windows.TablesWindow import TablesWindow
import sqlite3 as sql


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.init_main()

    def init_main(self):
        toolbar = tk.Frame(bg=const.toolbar_bg, bd=10)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_create_db = tk.Button(toolbar, text='Create database', command=self.open_create_db_dialog, bd=1,
                                  compound=tk.TOP)

        btn_create_db.grid(row=0, column=0, ipadx=10, padx=10)

        btn_select_db = tk.Button(toolbar, text='Select database', command=self.open_selected_db,
                                  bd=1, compound=tk.TOP)
        btn_select_db.grid(row=0, column=1, ipadx=10, padx=10)

        btn_delete_db = tk.Button(toolbar, text='Delete database', command=self.delete_selected_db,
                                  bd=1, compound=tk.TOP)
        btn_delete_db.grid(row=0, column=2, ipadx=10, padx=10)

        btn_refresh_db = tk.Button(toolbar, text='Refresh', command=self.refresh_db,
                                  bd=1, compound=tk.TOP)
        btn_refresh_db.grid(row=0, column=3, ipadx=10, padx=10)


        scrollbar = tk.Scrollbar(self.root)
        self.db_list_box = tk.Listbox(self.root, yscrollcommand=scrollbar.set, height=15, width=103)
        self.db_list_box.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=self.db_list_box.yview)

        self.view_db_files()

    def open_create_db_dialog(self):
        DBCreationDialog(self.root)

    def open_selected_db(self):
        selected = self.db_list_box.get(self.db_list_box.curselection())
        db_name = selected[:-3]
        path = const.resource_path + selected
        connection = sql.connect(path)
        TablesWindow(self.root, db_name=db_name, db_connection=connection)

    def refresh_db(self):
        self.view_db_files()

    def delete_selected_db(self):
        selected = self.db_list_box.get(self.db_list_box.curselection())
        path = const.resource_path + selected
        FileReader.delete_db_file(path)
        self.view_db_files()

    def view_db_files(self):
        self.db_list_box.delete(0, tk.END)
        file_names = FileReader.get_db_file_names()
        for i in file_names:
            self.db_list_box.insert(tk.END, i)
