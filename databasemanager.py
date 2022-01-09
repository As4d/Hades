import pyodbc
import json


class DatabaseManager:  
    def __init__(self):
        self.connectionString = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:hadesdemo.database.windows.net;PORT=1433;database=hadesdemo;uid=hadesdemoadmin;pwd=AM?z5#r$"

    def updateIntoUser(
        self,
        UserId,
        IpAddress,
        TotalFileCount,
        LastScan,
        OperatingSystem,
        NumberOfScans,
    ):

        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE [User] SET IpAddress = ?, TotalFileCount = ?, LastScan = ?, OperatingSystem = ?, NumberOfScans = ? WHERE UserId = ?",
                    [
                        IpAddress,
                        TotalFileCount,
                        LastScan,
                        OperatingSystem,
                        NumberOfScans,
                        UserId,
                    ],
                )
        

    def insertIntoUser(
        self,
        UserId,
        IpAddress,
        TotalFileCount,
        LastScan,
        OperatingSystem,
        NumberOfScans,
    ):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO [User] VALUES (?,?,?,?,?,?)",
                    [
                        UserId,
                        IpAddress,
                        TotalFileCount,
                        LastScan,
                        OperatingSystem,
                        NumberOfScans,
                    ],
                )
        

    def updateIntoUserFiles(self, UserId, FileType, FileCount):
        self.db.execute(
            """UPDATE UserFiles SET FileCount = ? WHERE UserId = ? AND FileType = ?""",
            [FileCount, UserId, FileType],
        )
        
        if self.db.rowcount == 0:
            self.insertIntoUserFiles(UserId, FileType, FileCount)

    def insertIntoUserFiles(self, UserId, FileType, FileCount):
        self.db.execute(
            "INSERT INTO UserFiles VALUES (NULL,?,?,?)",
            [UserId, FileType, FileCount],
        )
        self.connection.commit()

    def updateUser(self):
        FH = open("User.json")
        data = json.load(FH)
        try:

            self.insertIntoUser(
                data["NetworkInfo"]["UserId"],
                data["NetworkInfo"]["ipv4"],
                data["FileCounts"]["total"],
                data["ScanInfo"]["LastScan"],
                data["OS"]["system"],
                data["ScanInfo"]["ScanCount"],
            )

        except:

            self.updateIntoUser(
                data["NetworkInfo"]["UserId"],
                data["NetworkInfo"]["ipv4"],
                data["FileCounts"]["total"],
                data["ScanInfo"]["LastScan"],
                data["OS"]["system"],
                data["ScanInfo"]["ScanCount"],
            )

    def updateUserFiles(self):
        FH = open("User.json")
        data = json.load(FH)

        for type in data["FileCounts"]:
            if type == "total":
                break
            else:
                self.updateIntoUserFiles(
                    data["NetworkInfo"]["UserId"], type, data["FileCounts"][type]
                )