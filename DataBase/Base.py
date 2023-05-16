from DataBase.Table import Table
import constants as const
import itertools


class Base:
    def __init__(self, db_controller):
        self.db_controller = db_controller
        self.tables = list()
        self.name_pos_table = dict() # a dictionary of table names and their positions in the self.tables list

    def get_common_attrs(self, table1, table2):
        tbl1_attrs = []
        tbl2_attrs = []
        cursor = self.db_controller.cursor

        cursor.execute("SELECT * FROM " + const.attr_table + " WHERE " + const.attr_table_name
                       + " = " + "?" + ";", (table1,))

        rows = cursor.fetchall()
        for row in rows:
            tbl1_attrs.append(row[1].lower())

        cursor.execute("SELECT * FROM " + const.attr_table + " WHERE " + const.attr_table_name
                       + " = " + "?" + ";", (table2,))
        rows = cursor.fetchall()
        for row in rows:
            tbl2_attrs.append(row[1].lower())

        return list(set(tbl1_attrs) & set(tbl2_attrs))

    def get_join_table(self, comm_attr, tbl1, tbl2):
        def concat_row(r1, r2):
            result_row = []
            for cell in r1.cells:
                result_row.append(cell.val)
            for cell in r2.cells:
                if cell.name_attr.lower() == comm_attr:
                    continue
                result_row.append(cell.val)

            return result_row

        table1 = self.db_controller.get_records(tbl1)
        table2 = self.db_controller.get_records(tbl2)

        table1_comm_attr_values = set()
        self._set_comm_attr_values(comm_attr, table1, table1_comm_attr_values)

        table2_comm_attr_values = set()
        self._set_comm_attr_values(comm_attr, table2, table2_comm_attr_values)

        result_comm_attr_values = table1_comm_attr_values & table2_comm_attr_values

        res_table = Table(tbl1 + " join " + tbl2)

        self._fill_res_table(comm_attr, concat_row, res_table, result_comm_attr_values, table1, table2)

        return res_table

    def _fill_res_table(self, comm_attr, concat_row, res_table, result_comm_attr_values, table1, table2):
        for row1, row2 in itertools.product(table1.rows, table2.rows):
            for cell1, cell2 in itertools.product(row1.cells, row2.cells):
                if self._is_mathcing_cell(cell1, comm_attr) and cell1.val in result_comm_attr_values and \
                        self._is_mathcing_cell(cell2, comm_attr) and cell2.val == cell1.val:
                    res_table.add_row(concat_row(row1, row2))

    def _is_mathcing_cell(self, cell, comm_attr):
        return cell.name_attr.lower() == comm_attr.lower()

    def _set_comm_attr_values(self, comm_attr, table, table_comm_attr_values):
        for row in table.rows:
            for cell in row.cells:
                if self._is_mathcing_cell(cell, comm_attr):
                    table_comm_attr_values.add(cell.val)

    def create_table(self, table):
        self.tables.append(table)
        self.name_pos_table[table.name] = len(self.tables)

    def get_table(self, table_name):
        return self.tables[self.name_pos_table[table_name]]