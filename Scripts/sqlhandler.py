import pyodbc
# old, so not PEP8 compliant, sorry.
class SQLHandler:
    
    def __init__(self, currentserver, database):
        """The class responsible for SQL queries.
            Args:
                currentserver(str) - the server name to connect to. Specified in config.txt
                database(str) - the database in the server, specified in config.txt
                currentpath(str) - the current file path.
            Returns:
                SQLhandler
        """
        
        self.currentserver = currentserver
        #Sets up the connection
        self.connection = pyodbc.connect("DRIVER={SQL Server};SERVER="+currentserver+";DATABASE="+database+";Trusted_Connection=yes", timeout=5)
        self.connection.timeout=5
        self.cursor = self.connection.cursor()
        self.connection.execute("SET NOCOUNT ON;")
        self.createTables()
        
    def createTables(self):
        """When the intiial connection to the database is made, a check will be made for each table that is needed - if the table is not existing or has no data,
        we will add example records to each table after creating the table. This means that the program can be 'plugged' into a database and automatically format it to store the correct data,
        without any manual SQL work."""
        #INSERT TABLES CHECK HERE
        # Table name: table creation script
        TableQueries = {

        }

        for key in TableQueries:

            self.addToDatabase(f"""IF NOT EXISTS(SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = N'{key}') 
            BEGIN 
            {TableQueries[key]}
            
            END;""")

        
            

    def queryDatabase(self, query: str) -> tuple:
        """Internal command used to query the current database, and return the results of the query. If an error occurs, an error window is displayed.
        Args:
            query(str) - the SQL query to be executed.
        Returns:
            tuple(tuple) - A tuple containing all the records in tuple form ((r1col1, r1col2), (r2col1, r2col2)...)
            
        """


        try:
            #Executes the query input
            self.cursor.execute(query)
            #returns the results
            return self.cursor.fetchall()
        except pyodbc.OperationalError:
            #The error is likely to be a network error (loss of connection), so we will return this here
            #main.win.displayNetworkError()
            return
    def addToDatabase(self, query: str):
        """Commits changes using connection.commit(), so should be used for them. Returns False if an error occurs, as well as the error.
            Args:
                query(str) - the SQL query to be executed.
            Returns:
                tuple(boolean, exception) - A tuple of the boolean for whether the execution was successful, and the exception returned (or "placeholder_exception" if no exception)
            
        """

        try:
            try:

                self.connection.execute(query)
                #Commits the executed query to ensure changes are made.
                self.connection.commit()
                return True, "placeholder_exception"
            except pyodbc.OperationalError as e:
                return False, e
        except Exception as e:
            return False, e