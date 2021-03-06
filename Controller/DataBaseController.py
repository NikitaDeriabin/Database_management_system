import sqlite3 as sql
import constants as const
from DataBase.Table import Table
from DataBase.Row import Row
from DataBase.Cell import Cell
from DataBase.Attribute import Attribute


class DataBaseController:
    @staticmethod
    def create_db(name):
        def create_attr_table(db_path):
            connection = sql.connect(db_path)
            cursor = connection.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS attribute(
                name_table TEXT,
                col_name TEXT,
                 type_name TEXT);
            """)
            connection.commit()

        file_path = const.resource_path + name
        file = open(file_path + ".db", "a")
        file.close()
        create_attr_table(file_path+".db")

    @staticmethod
    def get_table_data(tb_name, db_connection):
        table = Table(tb_name)
        cursor = db_connection.cursor()

        cursor.execute("SELECT * FROM " + const.attr_table + " WHERE " + const.attr_table_name
                       + " = " + "?" + ";", (tb_name,))
        attr_records = cursor.fetchall()
        for rec in attr_records:
            attr = Attribute(table_name=rec[0], name=rec[1], data_type=rec[2])
            table.add_attribute(attr)

        return table

    @staticmethod
    def get_records(tb_name, db_connection):
        table = DataBaseController.get_table_data(tb_name, db_connection)
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM " + tb_name + ";")
        table_records = cursor.fetchall()

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

    @staticmethod
    def insert_row(db_connection, table, row):
        cursor = db_connection.cursor()
        request_str = "INSERT INTO " + table.name + " ("
        for cell in row.cells:
            request_str += cell.name_attr + ", "
        request_str = request_str[:-2] + ") VALUES ("
        for i in range(len(row.cells)):
            request_str += "?, "
        request_str = request_str[:-2] + ")"

        insert_values = tuple([cell.val for cell in row.cells])

        cursor.execute(request_str, insert_values)
        db_connection.commit()

    @staticmethod
    def update_row(db_connection, table, row, row_id):
        cursor = db_connection.cursor()
        request_str = "UPDATE " + table.name + " SET "

        for cell in row.cells:
            request_str += cell.name_attr + "=?, "
        request_str = request_str[:-2] + " WHERE id=?"

        insert_values = tuple([cell.val for cell in row.cells] + [row_id])

        cursor.execute(request_str, insert_values)
        db_connection.commit()

    @staticmethod
    def delete_row(db_connection, table, rows):
        cursor = db_connection.cursor()
        request_str = "DELETE FROM " + table.name + " WHERE id=?;"
        for row in rows:
            cursor.execute(request_str, (row,))

        db_connection.commit()
