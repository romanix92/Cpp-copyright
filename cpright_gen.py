#!/usr/bin/python

import sys
import re
import os
import datetime

args = list(sys.argv)
print("Files to be processed:\n", args[1:len(args)], "\nTotal:", len(args)-1)
company = input("Enter company name: ")
authors = input("Enter authors: ")

for filename in args[1:len(args)]:
    try:
        with open(filename) as fd:
            orig = fd.read()
            date = datetime.datetime.fromtimestamp(os.path.getmtime(filename)).strftime("%x %X")
    except IOError:
        print("Cannot open file ", filename)
        continue
    with open(filename, "w") as fd:
        fd.write("/*******************************************************************************\n")
        fd.write(" * Copyright: " + company + ". All rights reserved.\n")
        fd.write(" * File name: " + re.search("[^/]*$", filename).group() + "\n")
        fd.write(" * Authors  : " + authors + "\n")
        fd.write(" * Modification date: " + date + "\n")
        classes = re.findall('(?<=class\s)\w+', orig)
        fd.write(" * Classes: " + str(classes) + "\n")
        fd.write(" * Description: TODO\n")
        fd.write(" *******************************************************************************/\n\n")
        fd.write(orig)

