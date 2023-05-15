import unittest
from Controller.DatabaseController import DatabaseController
import constants as const
from DataBase.Base import Base
from DataBase.DataTypes import DataType
import os



class TestWork(unittest.TestCase):
    def setUp(self):
        db_name = "test"
        try:
            os.remove(const.resource_path + db_name + ".db")
        except:
            pass

        self._create_test_database(db_name)

        self.db_controller = DatabaseController(path=const.resource_path + db_name + ".db")


        self.db_controller.cursor.execute("""CREATE TABLE IF NOT EXISTS Person (
                id integer PRIMARY KEY,
                name TEXT,
                surname TEXT,
                age TEXT);""")

        self.db_controller.cursor.execute("""CREATE TABLE IF NOT EXISTS Student (
                        id integer PRIMARY KEY,
                        surname TEXT,
                        class TEXT,
                        average_score TEXT);""")

        self.db_controller.cursor.execute("""INSERT INTO """ + const.attr_table + " (" + \
                                     const.attr_table_name + ", " + const.attr_table_column_name + ", " + \
                                     const.attr_table_type + ")" + " VALUES (?, ?, ?)",
                                     ("Person", "name", DataType.STRING))

        self.db_controller.cursor.execute("""INSERT INTO """ + const.attr_table + " (" + \
                                     const.attr_table_name + ", " + const.attr_table_column_name + ", " + \
                                     const.attr_table_type + ")" + " VALUES (?, ?, ?)",
                                     ("Person", "surname", DataType.STRING))

        self.db_controller.cursor.execute("""INSERT INTO """ + const.attr_table + " (" + \
                                     const.attr_table_name + ", " + const.attr_table_column_name + ", " + \
                                     const.attr_table_type + ")" + " VALUES (?, ?, ?)",
                                     ("Person", "age", DataType.INT))

        self.db_controller.cursor.execute("""INSERT INTO """ + const.attr_table + " (" + \
                                     const.attr_table_name + ", " + const.attr_table_column_name + ", " + \
                                     const.attr_table_type + ")" + " VALUES (?, ?, ?)",
                                     ("Student", "surname", DataType.STRING))

        self.db_controller.cursor.execute("""INSERT INTO """ + const.attr_table + " (" + \
                                     const.attr_table_name + ", " + const.attr_table_column_name + ", " + \
                                     const.attr_table_type + ")" + " VALUES (?, ?, ?)",
                                     ("Student", "class", DataType.STRING))

        self.db_controller.cursor.execute("""INSERT INTO """ + const.attr_table + " (" + \
                                     const.attr_table_name + ", " + const.attr_table_column_name + ", " + \
                                     const.attr_table_type + ")" + " VALUES (?, ?, ?)",
                                     ("Student", "average_score", DataType.REAL))

        self.db_controller.connection.commit()

        self.db_controller.cursor.execute("""INSERT INTO Person (name, surname, age) VALUES (
                        ?, ?, ?);""", ("Bob", "Bobson", "20"))
        self.db_controller.cursor.execute("""INSERT INTO Person (name, surname, age) VALUES (
                                ?, ?, ?);""", ("Peter", "Peterson", "21"))
        self.db_controller.cursor.execute("""INSERT INTO Person (name, surname, age) VALUES (
                                ?, ?, ?);""", ("Steve", "Stevenson", "20"))
        self.db_controller.cursor.execute("""INSERT INTO Person (name, surname, age) VALUES (
                                ?, ?, ?);""", ("Leo", "Leojinio", "19"))
        self.db_controller.cursor.execute("""INSERT INTO Person (name, surname, age) VALUES (
                                ?, ?, ?);""", ("Robert", "Robertson", "22"))

        self.db_controller.connection.commit()

        self.db_controller.cursor.execute("""INSERT INTO Student (surname, class, average_score) VALUES (
                                ?, ?, ?);""", ("Bobson", "atp-1", "43.2"))

        self.db_controller.cursor.execute("""INSERT INTO Student (surname, class, average_score) VALUES (
                                        ?, ?, ?);""", ("Peterson", "akc-2", "33.2"))

        self.db_controller.cursor.execute("""INSERT INTO Student (surname, class, average_score) VALUES (
                                        ?, ?, ?);""", ("Stevenson", "por-4", "45.2"))

        self.db_controller.connection.commit()

    def tearDown(self):
        try:
            self.db_controller.cursor.close()
            self.db_controller.connection.close()
            DatabaseController.clear()
            os.remove(const.resource_path + "test.db")
        except Exception as e:
            raise Exception(e)

    def test_lvnl_money_validation(self):
        values = ["dfdsjk", "234$;2342.234$", "21$;", "123.$;43$"]
        for i in values:
            with self.subTest(i=i):
                with self.assertRaises(TypeError) as err:
                    DataType.validate_lnvl_money('some attribute', i)
                self.assertEqual("Invalid type on attr 'some attribute'. Must be lvnl_money!", err.exception.args[0])

    def test_get_common_attr_of_tables(self):

        table1 = "Person"
        table2 = "Student"

        db = Base(self.db_controller)
        res = db.get_common_attrs(table1, table2)
        self.assertEqual('surname', res[0])

    def _create_test_database(self, db_name):
        DatabaseController.create_db(db_name)

    def test_join_tables(self):
        table1 = "Person"
        table2 = "Student"

        db = Base(self.db_controller)
        comm_attr = db.get_common_attrs(table1, table2)
        table_to_check = db.get_join_table(comm_attr[0], table1, table2)

        self.assertTrue(len(table_to_check.rows) == 3)
        self.assertEqual('Bob', table_to_check.rows[0][0])
        self.assertEqual('Peter', table_to_check.rows[1][0])
        self.assertEqual('Steve', table_to_check.rows[2][0])

