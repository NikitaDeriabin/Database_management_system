import sqlite3 as sql
import constants as const
from DataBase.Table import Table
from DataBase.Row import Row
from DataBase.Cell import Cell
from DataBase.Attribute import Attribute


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        path = kwargs['path']
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        elif path != cls._instances[cls].path:
            cls._instances[cls].cursor.close()
            cls._instances[cls].connection.close()
            cls._instances[cls].__init__(*args, **kwargs)

        return cls._instances[cls]

    def clear(cls):
        cls._instances = {}

class DatabaseController(metaclass=Singleton):

    def __init__(self, path=None):
        self.path = path
        self.connection = sql.connect(path)
        self.cursor = self.connection.cursor()

    @staticmethod
    def _create_db_storage_file(file_name: str):
        file_path = const.resource_path + file_name
        file = open(file_path + ".db", "a")
        file.close()
        return file_path

    @staticmethod
    def create_db(name: str):
        def create_attr_table(db_path):
            connection = sql.connect(db_path)
            cursor = connection.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS attribute(
                name_table TEXT,
                col_name TEXT,
                 type_name TEXT);
            """)
            connection.commit()

            cursor.close()
            connection.close()

        file_path = DatabaseController._create_db_storage_file(name)
        create_attr_table(file_path+".db")


    def get_table_data(self, tb_name):
        table = Table(tb_name)

        self.cursor.execute("SELECT * FROM " + const.attr_table + " WHERE " + const.attr_table_name
                       + " = " + "?" + ";", (tb_name,))
        attr_records = self.cursor.fetchall()

        for rec in attr_records:
            attr = Attribute(table_name=rec[0], name=rec[1], data_type=rec[2])
            table.add_attribute(attr)

        return table

    def get_records(self, tb_name):
        table = self.get_table_data(tb_name)
        self.cursor.execute("SELECT * FROM " + tb_name + ";")
        table_records = self.cursor.fetchall()

        for rec in table_records:
            row_list = []

            for i in enumerate(table.attributes):
                cell = Cell(name_attr=i[1].name, type_attr=i[1].type)
                cell.set_val(rec[i[0] + 1])
                row_list.append(cell)

            row = Row(len(table.attributes))
            row.set_cells(row_list)
            table.add_row(row)

        return table

    def insert_row(self, table, row):
        request_str = "INSERT INTO " + table.name + " ("
        for cell in row.cells:
            request_str += cell.name_attr + ", "
        request_str = request_str[:-2] + ") VALUES ("
        for i in range(len(row.cells)):
            request_str += "?, "
        request_str = request_str[:-2] + ")"

        insert_values = tuple([cell.val for cell in row.cells])

        self.cursor.execute(request_str, insert_values)
        self.connection.commit()

    def update_row(self, table, row, row_id):
        request_str = "UPDATE " + table.name + " SET "

        for cell in row.cells:
            request_str += cell.name_attr + "=?, "
        request_str = request_str[:-2] + " WHERE id=?"

        insert_values = tuple([cell.val for cell in row.cells] + [row_id])

        self.cursor.execute(request_str, insert_values)
        self.connection.commit()

    def delete_row(self, table, rows):
        request_str = "DELETE FROM " + table.name + " WHERE id=?;"
        for row in rows:
            self.cursor.execute(request_str, (row,))

        self.connection.commit()
