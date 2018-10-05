""""file containing functions that interact with the database."""
# connection_url = """database='mydiary', user='postgres',
#                  password= 'actuarial', host='127.0.0.1',  port='5432'"""

from datetime import datetime, timedelta
import psycopg2.extensions


try:
    connection = psycopg2.connect(database="mydiary", user="postgres",
                                  password="actuarial", host="127.0.0.1",
                                  port="5432")
    my_cursor = connection.cursor()
except psycopg2.DatabaseError:
    print("Database connection failed!")


############################################################################
class CreateTables:
    """Class used to create tables"""
    @property
    def create_user_table(self):
        """Helper function used to create the user_table"""
        sql_statement = '''CREATE TABLE IF NOT EXISTS USERS
                (ID                 SERIAL    PRIMARY KEY,
                FIRSTNAME           TEXT      NOT NULL,
                LASTNAME            TEXT      NOT NULL,
                USERNAME            TEXT      NOT NULL UNIQUE,
                EMAIL               TEXT      NOT NULL UNIQUE,
                PASSWORD            TEXT      NOT NULL,
                DATETIMEREGISTERED  TIMESTAMP NOT NULL);'''
        user_table = my_cursor.execute(sql_statement)
        connection.commit()
        return user_table

    @property
    def create_entries_table(self):
        """Helper function used to create an entries table."""
        sql_statement = '''CREATE TABLE IF NOT EXISTS ENTRIES
                        (ID             SERIAL      PRIMARY KEY,
                        TITLE           TEXT        NOT NULL,
                        CONTENTS        TEXT        NOT NULL,
                        DATEOFEVENT     TIMESTAMP   NOT NULL,
                        TIMETOMODIFY    TIMESTAMP   NOT NULL,
                        REMINDERTIME    TIMESTAMP   NOT NULL,
                        USERID      INT REFERENCES USERS ON DELETE CASCADE);'''
        entries_table = my_cursor.execute(sql_statement)
        connection.commit()
        print("entries table created.")
        return entries_table

#####################################################################


class OperateDatabase(CreateTables):
    """Class used to interact with the database"""

    def check_user_in_database(self, email, password):
        """Helper method used to check if a user is in the database"""
        sql_statement = """SELECT ID FROM USERS WHERE EMAIL = %s AND
                        PASSWORD = %s;"""
        user_id = my_cursor.execute(self, sql_statement, (email, password,))
        connection.commit()(self)
        if user_id:
            return user_id
        return False

    def create_user(self, email, username, *args):
        """Helper function used to create a user"""
        sql_statement = """SELECT ID FROM USERS WHERE EMAIL = %s OR
                         USERNAME = %s;"""
        user_in_database = my_cursor.execute(self, sql_statement, (email,
                                                                   username,))

        sql_statement2 = """INSERT INTO USERS (FIRSTNAME, LASTNAME, USERNAME,
                         EMAIL, PASSWORD, DATETIMEREGISTERED)
                         VALUES (%s, %s, %s, %s, %s, %s);"""
        if not user_in_database:
            my_cursor.execute(self, sql_statement2, *args)
            connection.commit()(self)
            return True
        return False

    def create_entry(self, *args):
        """Helper function used to create a diary entry."""
        sql_statement = """INSERT INTO ENTRIES (TITLE, CONTENTS,
                          DATEOFEVENT, TIMETOMODIFY, REMINDERTIME, USERID)
                          VALUES (%s, %s, %s, %s, %s, %s);"""
        my_cursor.execute(sql_statement, *args)
        connection.commit()
        return True

    def update_entry(self, entry_id, user_id, *args):
        """Helper function used to update a diary entry."""
        sql_statement = """SELECT ID FROM ENTRIES WHERE ID = %s AND
                         USERID = %s;"""
        my_cursor.execute(sql_statement, (entry_id, user_id,))
        entry_in_database = my_cursor.fetchone()
        sql_statement2 = """UPDATE ENTRIES SET TITLE = %s, CONTENTS = %s,
                         DATEOFEVENT = %s, REMINDERTIME = %s WHERE ID = %s
                         AND USERID = %s;"""
        if entry_in_database:
            print("The entry database is", entry_in_database)
            my_cursor.execute(sql_statement2, *args)
            connection.commit()
            return True
        connection.commit()
        return False


    def remove_entry(self, entry_id, user_id):
        """Helper function used to delete a diary entry."""
        my_cursor.execute("""SELECT ID FROM ENTRIES WHERE ID = %s AND
                         USERID = %s;""", (entry_id, user_id,))
        entry_in_database = my_cursor.fetchone()
        if entry_in_database:
            my_cursor.execute("""DELETE FROM ENTRIES WHERE ID = %s
                              AND USERID = %s""", (entry_id, user_id,))
            connection.commit()
            return True
        return False

    def get_one_user_entry(self, entry_id, user_id):
        my_cursor.execute("""SELECT TITLE, CONTENTS, DATEOFEVENT, REMINDERTIME
                          FROM ENTRIES WHERE ID = %s AND USERID = %s;""",
                          (entry_id, user_id,))
        one_entry = my_cursor.fetchone()
        if one_entry:
            return one_entry
        return False

    def get_all_entries(self, entry_id, user_id):
        my_cursor.execute("""SELECT TITLE, CONTENTS, DATEOFEVENT, REMINDERTIME
                          FROM ENTRIES WHERE ID = %s AND USERID = %s
                          ORDER BY ID;""", (entry_id, user_id,))
        all_entries = my_cursor.fetchall()
        if all_entries:
            return all_entries
        return False

    def get_user_details(self, user_id):
        my_cursor.execute("""SELECT FIRSTNAME, LASTNAME, USERNAME,EMAIL
                          FROM USERS WHERE ID = %s;""", (user_id,))
        one_entry = my_cursor.fetchall()
        if one_entry:
            return one_entry
        return False
