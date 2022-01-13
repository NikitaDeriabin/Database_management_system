import unittest
import sqlite3
from Controller.DataBaseController import DataBaseController
import constants as const
from DataBase.Base import Base
from DataBase.DataTypes import DataType
import os


def setUp(self):
    try:
        os.remove(const.resource_path + "test.db")
    except:
        pass

    DataBaseController.create_db("test")

    self.db_connection = sqlite3.connect(const.resource_path + 'test.db')
    cursor = self.db_connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS Person (
            id integer PRIMARY KEY,
            name TEXT,
            surname TEXT,
            age TEXT);""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS Student (
                    id integer PRIMARY KEY,
                    surname TEXT,
                    class TEXT,
                    average_score TEXT);""")

    cursor.execute("""INSERT INTO """ + const.attr_table + " (" + \
                   const.attr_table_name + ", " + const.attr_table_column_name + ", " + \
                   const.attr_table_type + ")" + " VALUES (?, ?, ?)",
                   ("Person", "name", DataType.STRING))

    cursor.execute("""INSERT INTO """ + const.attr_table + " (" + \
                   const.attr_table_name + ", " + const.attr_table_column_name + ", " + \
                   const.attr_table_type + ")" + " VALUES (?, ?, ?)",
                   ("Person", "surname", DataType.STRING))

    cursor.execute("""INSERT INTO """ + const.attr_table + " (" + \
                   const.attr_table_name + ", " + const.attr_table_column_name + ", " + \
                   const.attr_table_type + ")" + " VALUES (?, ?, ?)",
                   ("Person", "age", DataType.INT))

    cursor.execute("""INSERT INTO """ + const.attr_table + " (" + \
                   const.attr_table_name + ", " + const.attr_table_column_name + ", " + \
                   const.attr_table_type + ")" + " VALUES (?, ?, ?)",
                   ("Student", "surname", DataType.STRING))

    cursor.execute("""INSERT INTO """ + const.attr_table + " (" + \
                   const.attr_table_name + ", " + const.attr_table_column_name + ", " + \
                   const.attr_table_type + ")" + " VALUES (?, ?, ?)",
                   ("Student", "class", DataType.STRING))

    cursor.execute("""INSERT INTO """ + const.attr_table + " (" + \
                   const.attr_table_name + ", " + const.attr_table_column_name + ", " + \
                   const.attr_table_type + ")" + " VALUES (?, ?, ?)",
                   ("Student", "average_score", DataType.REAL))

    self.db_connection.commit()

    cursor.execute("""INSERT INTO Person (name, surname, age) VALUES (
                    ?, ?, ?);""", ("Bob", "Bobson", "20"))
    cursor.execute("""INSERT INTO Person (name, surname, age) VALUES (
                            ?, ?, ?);""", ("Peter", "Peterson", "21"))
    cursor.execute("""INSERT INTO Person (name, surname, age) VALUES (
                            ?, ?, ?);""", ("Steve", "Stevenson", "20"))
    cursor.execute("""INSERT INTO Person (name, surname, age) VALUES (
                            ?, ?, ?);""", ("Leo", "Leojinio", "19"))
    cursor.execute("""INSERT INTO Person (name, surname, age) VALUES (
                            ?, ?, ?);""", ("Robert", "Robertson", "22"))

    self.db_connection.commit()

    cursor.execute("""INSERT INTO Student (surname, class, average_score) VALUES (
                            ?, ?, ?);""", ("Bobson", "atp-1", "43.2"))

    cursor.execute("""INSERT INTO Student (surname, class, average_score) VALUES (
                                    ?, ?, ?);""", ("Peterson", "akc-2", "33.2"))

    cursor.execute("""INSERT INTO Student (surname, class, average_score) VALUES (
                                    ?, ?, ?);""", ("Stevenson", "por-4", "45.2"))

    self.db_connection.commit()

    cursor.close()


class TestWork(unittest.TestCase):

    def tearDown(self):
        try:
            os.remove(const.resource_path + "test.db")
        except:
            pass

    def test_lvnl_money_validation(self):
        values = ["dfdsjk", "234$;2342.234$", "21$;", "123.$;43$"]
        for i in values:
            with self.subTest(i=i):
                with self.assertRaises(TypeError) as err:
                    DataType.validate_lnvl_money('some attribute', i)
                self.assertEqual("Invalid type on attr 'some attribute'. Must be lvnl_money!", err.exception.args[0])

    def test_get_common_attr_of_tables(self):
        setUp(self)

        table1 = "Person"
        table2 = "Student"

        db = Base(self.db_connection)
        res = db.get_common_attrs(table1, table2)
        self.assertEqual('surname', res[0])

    def test_join_tables(self):

        setUp(self)
        table1 = "Person"
        table2 = "Student"

        db = Base(self.db_connection)
        comm_attr = db.get_common_attrs(table1, table2)
        table_to_check = db.get_join_table(comm_attr[0], table1, table2)

        self.assertTrue(len(table_to_check.rows) == 3)
        self.assertEqual('Bob', table_to_check.rows[0][0])
        self.assertEqual('Peter', table_to_check.rows[1][0])
        self.assertEqual('Steve', table_to_check.rows[2][0])

