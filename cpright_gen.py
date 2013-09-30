#!/usr/bin/python

import sys, re, os, datetime

class ArgParser:
    @staticmethod
    def ParseArgs(args):
        data = ArgsData()
        for arg in args[1:len(args)]:
            if arg.startswith("--author="):
                data.authors = arg.replace("--author=", "", 1)
            elif arg.startswith("--company="):
                data.company = arg.replace("--company=", "", 1)
            elif arg.startswith("--mode="):
                data.mode = arg.replace("--mode=", "", 1)
            else:
                data.files.append(arg)
        return data

class ArgsData:
    def __init__(self):
        self.authors = ""
        self.company = ""
        self.mode    = ""
        self.files   = []

class OldNotice:
    def __init__(self, oldNotice):
        self.company, self.authors, self.description = "", "", ""
        companyMatch = re.search("[*] Copyright: (.*)[.] All rights", oldNotice)
        if companyMatch is not None:
            self.company = companyMatch.group(1)
        authorsMatch = re.search("[*] Authors  : (.*)", oldNotice)
        if authorsMatch is not None:
            self.authors = authorsMatch.group(1)
        descriptionMatch = re.search("[*] Description: (.*) ([*]{78})", oldNotice, re.S)
        if descriptionMatch is not None:
            self.description = descriptionMatch.group(1)

class NoticeData:
    def __init__(self, mode):
        self.mode = mode
    def setData(self, text, argData):
        old = OldNotice(text)
        print(self.mode)
        if self.mode == "replace":
            self.authors = argData.authors if argData.authors else old.authors
            print(self.authors)
            self.company = argData.company if argData.company else old.company
        else:#update and default
            self.authors = old.authors if old.authors else argData.authors
            self.company = old.company if old.company else argData.company
        self.description = old.description if old.description else "TODO\n"


######   Script start   #######

argData = ArgParser.ParseArgs(list(sys.argv))
print("Files:")
print(argData.files)
notice = NoticeData(argData.mode)
oldNotice = re.compile("/[*]{79}.*[*]{78}/\s*", re.S)
classes = re.compile('(?<=class\s)\w+')

for filename in argData.files:
    try:
        with open(filename) as fd:
            orig = fd.read()
            date = datetime.datetime.fromtimestamp(os.path.getmtime(filename)).strftime("%x %X")
    except IOError:
        print("Cannot open file ", filename)
        continue
    with open(filename, "w") as fd:
        notice.setData(orig, argData)
        orig = oldNotice.sub("", orig)
        fd.write("/*******************************************************************************\n")
        fd.write(" * Copyright: %s. All rights reserved.\n" % notice.company)
        fd.write(" * File name: %s\n" % re.search("[^/]*$", filename).group())
        fd.write(" * Authors  : %s\n" %  notice.authors)
        fd.write(" * Modification date: %s\n" % date)
        foundClasses = classes.findall(orig)
        if foundClasses:
            fd.write(" * Classes: %s\n" % str(foundClasses))
        fd.write(" * Description: " + notice.description)
        fd.write(" ******************************************************************************/\n\n")
        fd.write(orig)
