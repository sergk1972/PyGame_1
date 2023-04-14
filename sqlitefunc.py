import sqlite3
from sqlite3 import Error
from PyQt5.QtWidgets import QMessageBox


class SqliteActions:

    def __init__(self):
        self.data = None
        self.db = None

    def sql_connection(self):  # db_file  creating and establishing connection
        try:
            self.db = sqlite3.connect('database.db')
            return self.db
        except Error as ex:
            error: QMessageBox | QMessageBox = QMessageBox()
            # (QMessageBox_Icon='Warning')
            error.setIcon(QMessageBox.Information)
            error.setWindowTitle('Database Error!')
            error.setText(f"Can't establish connection!\n{ex}")
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()

    def sql_table_create(self):  # database table creating
        try:
            cursor_sql = self.db.cursor()
            cursor_sql.execute(f"CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
                               f"name TEXT DEFAULT 'empty_space', score INTEGER DEFAULT 'empty_space') ")
            self.db.commit()
        except Error as ex:
            error: QMessageBox | QMessageBox = QMessageBox()
            # (QMessageBox_Icon='Warning')
            error.setIcon(QMessageBox.Information)
            error.setWindowTitle('Database Error!')
            error.setText(f"Database already exist!\n{ex}")
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()

    def sql_table_delete(self):  # database table creating
        try:
            cursor_sql = self.db.cursor()
            cursor_sql.execute(f"DROP table if exists players")
            self.db.commit()
        except Error as ex:
            error: QMessageBox | QMessageBox = QMessageBox()
            # (QMessageBox_Icon='Warning')
            error.setIcon(QMessageBox.Information)
            error.setWindowTitle('Database Error!')
            error.setText(f"Database already exist!\n{ex}")
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()

    def sql_insert_one(self, name, score):
        try:
            cursor_sql = self.db.cursor()
            cursor_sql.execute(
                f'INSERT INTO players(name, score) VALUES(?, ?)', (name, score))
            self.db.commit()
        except Error as ex:
            error: QMessageBox | QMessageBox = QMessageBox()
            # (QMessageBox_Icon='Warning')
            error.setIcon(QMessageBox.Information)
            error.setWindowTitle('Database Error!')
            error.setText(f"Can't insert data!\n{ex}")
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()

    def sql_fetch(self):  # show data
        try:
            cursor_sql = self.db.cursor()
            cursor_sql.execute(f'SELECT name, score FROM players')
            data = cursor_sql.fetchall()
            return data
        except Error as ex:
            print(ex)
