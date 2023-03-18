import sqlite3
# run to reset the database.


class SQLiteHandler:

    def __init__(self):
        """
        SQLite handler
        """

        # connect, implicitly creating the database if it does not exist.
        self.connection = sqlite3.connect("Database/ExamQuestions.db")
        self.cursor = self.connection.cursor()

    def Reset(self):
        """
        Reset database - drop tables then recreate them
        """
        self.DropTables()
        self.CreateTables()
        print("reset tables")

    def DropTables(self):
        """
        DROP TABLES
        """
        queries = [
            "DROP TABLE IF EXISTS PAPER;",
            "DROP TABLE IF EXISTS QUESTION;",
            "DROP TABLE IF EXISTS PARTS;",
            "DROP TABLE IF EXISTS IMAGES;",
            "DROP TABLE IF EXISTS QUESTIONTOPIC;"
        ]
        for query in queries:
            self.addToDatabase(query)

    def CreateTables(self):
        """
        Create the tables
        """
        queries = [
            """
            CREATE TABLE PAPER(
  PaperID VARCHAR(40) PRIMARY KEY NOT NULL,
  PaperComponent VARCHAR(15),
  PaperYear VARCHAR(4),
  PaperLevel VARCHAR(10)
);

            """,
            """
            CREATE TABLE QUESTION(
  QuestionID VARCHAR(50) PRIMARY KEY NOT NULL,
  PaperID VARCHAR(40),
  QuestionNumber INTEGER,
  QuestionContents TEXT,
  TotalMarks INTEGER
);

            """,
            """
            CREATE TABLE IMAGES(
  ImageID INTEGER PRIMARY KEY NOT NULL,
  QuestionID VARCHAR(50),
  ImageData BLOB
);

            """,
            """
            CREATE TABLE PARTS(
  PartID VARCHAR(60) PRIMARY KEY NOT NULL,
  QuestionID VARCHAR(50),
  PartNumber VARCHAR(10),
  PartContents TEXT,
  PartMarks INTEGER
);

            """,
            """
            CREATE TABLE QUESTIONTOPIC(
  QuestionTopicID VARCHAR(150),
  QuestionID VARCHAR(50),
  TopicID VARCHAR(100)
);
            """
        ]
        for query in queries:
            self.addToDatabase(query)

    def queryDatabase(self, query: str) -> tuple:
        """Internal command used to query the current database, and return the
        results of the query. If an error occurs, an error window is displayed.
        Args:
            query(str) - the SQL query to be executed.
        Returns:
            tuple(tuple) - A tuple containing all the records in tuple form
            ((r1col1, r1col2), (r2col1, r2col2)...)
        """

        # Executes the query input
        self.cursor.execute(query)
        # returns the results
        return self.cursor.fetchall()

    def addToDatabase(self, query: str):
        """Commits changes using connection.commit(),
        so should be used for them. Returns False if an error occurs,
        as well as the error.
            Args:
                query(str) - the SQL query to be executed.
            Returns:
                tuple(boolean, exception) - A tuple of the boolean for whether
                the execution was successful, and the exception returned
                (or "placeholder_exception" if no exception)

        """

        try:
            try:
                # print(query)
                self.connection.executescript(query)
                # Commits the executed query to ensure changes are made.
                self.connection.commit()
                return True, "placeholder_exception"
            except sqlite3.Error as e:
                print(e)
                return False, e
        except Exception as e:
            print(e)
            return False, e


if __name__ == "__main__":
    sqlsocket = SQLiteHandler()
    sqlsocket.Reset()
