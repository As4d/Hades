import os
import re
import pathlib
from user import UserInfo

class Scanner():
    def __init__(self, obj):
        self.fileHelper = obj
        self.VulnerableFileNameFlags = 0
        self.VulnerableFileNamePaths = []

    def findVulnerableFileNames(self, extension):
        temp = 0
        vulnerablestrings = [
            "password",
            "account",
            "statement",
            "bank",
            "passport",
            "drivers liscense",
            "pin",
        ]

        if extension in self.fileHelper.files.keys():
            for file in self.fileHelper.getFilesList(extension):
                temp = file[::-1].split("\\")[0]
                filename = temp[temp.find(".") + 1 :][::-1]
                for string in vulnerablestrings:
                    x = re.findall("(?i)({}):*s*".format(string), filename)
                    if x != []:
                        self.VulnerableFileNamePaths.append((x, file))
                        self.VulnerableFileNameFlags += 1
        else:          
            self.fileHelper.findAllFiles(extension)
            for file in self.fileHelper.getFilesList(extension):
                temp = file[::-1].split("\\")[0]
                filename = temp[temp.find(".") + 1 :][::-1]
                for string in vulnerablestrings:
                    x = re.findall("(?i)({}):*s*".format(string), filename)
                    if x != []:
                        self.VulnerableFileNamePaths.append((x, file))
                        self.VulnerableFileNameFlags += 1
    
    def getVulnerableFileNameFlags(self):
        return self.VulnerableFileNameFlags
    
    def setVulnerableFileNameFlags(self, item):
        self.VulnerableFileNameFlags = item
    
    def resetVulnerableFileNameFlags(self):
        self.VulnerableFileNameFlags = 0
    
    def getVulnerableFileNamePaths(self):
        return self.VulnerableFileNamePaths
    
    def resetVulnerableFileNamePaths(self):
        self.VulnerableFileNamePaths = []
