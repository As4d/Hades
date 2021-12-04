import json
import socket
import datetime
import platform
import sqlite3
import uuid
from infector import Infector

class UserInfo():

    def __init__(self):
        self.data = {
            'NetworkInfo': {'ipv4': '', 'MachineName': '', 'UserId' : ''},
            'OS' : {'system' : '', 'version' : ''},
            'ScanInfo': {'LastScan' : '', 'ScanCount': '1'},
            'FilesCounts' : {'total': '', 'txt' : '', 'zip' : '', 'exe' : ''}
            }
        self.infector = Infector()

    def updateAllInfo(self):
        self.updateOs()
        self.updateipv4()
        self.updateMachineName()
        self.updateUserId()
        
    def writeToJson(self):
        self.updateAllInfo()
        self.updateCounts() # DELETE
        self.updateScanInfo() # DELETE
        FH = open('User.json', 'w')
        FH.write(json.dumps(self.data, indent=4))
    
    def updateCounts(self):
        self.infector.findAllFiles()
        self.data['FilesCounts']['total'] = self.infector.getTotalNumberOfFiles()
        self.data['FilesCounts']['txt'] = self.infector.getNumberOfTxtFiles()
        self.data['FilesCounts']['exe'] = self.infector.getNumberOfExeFiles()
        self.data['FilesCounts']['zip'] = self.infector.getNumberOfZipFiles()

    def updateOs(self):
        self.data['OS']['system'] = platform.system()
        self.data['OS']['version'] = platform.version()

    def updateipv4(self):
        self.data['NetworkInfo']['ipv4'] = str(socket.gethostbyname(socket.gethostname()))

    def updateMachineName(self):
        self.data['NetworkInfo']['MachineName'] = str(socket.gethostname())

    def updateScanInfo(self):
        self.data['ScanInfo']['LastScan'] = str(datetime.datetime.now()).split(".")[0]
        try:
            FH = open('User.json')
            data = json.load(FH)
            self.data['ScanInfo']['ScanCount'] = str(int(data['ScanInfo']['ScanCount']) + 1)
        except:
            pass
    
    def updateUserId(self):
        try:
            FH = open('User.json')
            data = json.load(FH)
            if data['NetworkInfo']['UserId'] == '':
                self.data['NetworkInfo']['UserId'] = str(uuid.uuid4())
            else:
                self.data['NetworkInfo']['UserId'] = data['NetworkInfo']['UserId']
        except:
            self.data['NetworkInfo']['UserId'] = str(uuid.uuid4())

class DatabaseManager():

	def __init__(self):
		self.connection = sqlite3.connect('test.db')
		self.db = self.connection.cursor()

	def CREATE_TABLE(self):
		self.db.execute('''
		CREATE TABLE User (
			UserId UNIQUEIDENTIFIER NOT NULL PRIMARY KEY,
			IpAddress VARCHAR(15) NOT NULL,
			TotalFileCount INT NOT NULL,
			LastScan DATETIME  NOT NULL,
			OperatingSystem VARCHAR(30) NOT NULL,
			NumberOfScans INT NOT NULL
		);
		''')

		self.db.execute('''
		CREATE TABLE UserFiles (
			Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
			UserId INT NOT NULL,
			FileType VARCHAR(4) not NULL,
			FileCount INT NOT NULL
		);
		''')
	
	def INSERT_INTO_User(self, UserId, IpAddress, TotalFileCount, LastScan, OperatingSystem, NumberOfScans):
		self.db.execute('INSERT INTO User VALUES (?,?,?,?,?,?)', [UserId, IpAddress, TotalFileCount, LastScan, OperatingSystem, NumberOfScans])
		self.connection.commit()
	
	def INSERT_INTO_UserFiles(self, UserId, TotalFileCount, FileType, FileCount):
		self.db.execute('INSERT INTO UserFiles VALUES (NULL,?,?,?,?)', [UserId, TotalFileCount, FileType, FileCount])
		self.connection.commit()

	def SELECT_User(self):
		print("==================== DATABASE TABLE User ====================")
		for row in self.db.execute('SELECT * FROM User'):
			print(row)

	def SELECT_UserFiles(self):
		print("==================== DATABASE TABLE UserFiles ====================")
		for row in self.db.execute('SELECT * FROM UserFiles'):
			print(row)
	
	def updateUser(self):
			FH = open('User.json')
			data = json.load(FH)
			self.INSERT_INTO_User(
                  data['NetworkInfo']['UserId'],
				  data['NetworkInfo']['ipv4'],
				  data['FilesCounts']['total'],
				  data['ScanInfo']['LastScan'],
				  data['OS']['system'],
				  data['ScanInfo']['ScanCount'])
	
	def updateUserFiles(self):
		try:
			FH = open('User.json')
			data = json.load(FH)
			print(
				  data['NetworkInfo']['ipv4'],
				  data['FilesCounts']['total'],
				  data['FilesCounts']['LastScan'],
				  data['FilesCounts']['system'])
		except:
			UserInfo().writeToJson()
			FH = open('User.json')
			data = json.load(FH)
			print(
				  data['NetworkInfo']['ipv4'],
				  data['FilesCounts']['total'],
				  data['FilesCounts']['LastScan'],
				  data['FilesCounts']['system'])


UserInfo().writeToJson()

DatabaseManager().updateUser()
