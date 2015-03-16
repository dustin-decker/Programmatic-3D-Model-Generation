#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      user
#
# Created:     26/08/2014
# Copyright:   (c) user 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
##import FreeCAD
##import Part
##import Mesh
import subprocess
import sys
import csv
import itertools

def worklist():
    """Worklist function converts a csv file into a dictionary with the key b
    being the item id and the values being the column values. Following this
    it calls the generate and convert functions if they are specified."""
    model_fn = 'ex.scad'
    generateset = 1 #1 if converting, 0 if not.
    convertset = 1 #1 if converting, 0 if not.

    d={}
    for i, row in enumerate(csv.reader(open('data.csv'))):
        if i==0: #grab our header
            header=row
            print header
        else:
            print row
            drow=dict(zip(header, row)) #zip our header and values together
            d[drow['id']]=drow #dict in a id dict
    if generateset == 1:    #call the generate function if set
        generate(d,header,model_fn,convertset)


def generate(d,header,model_fn,convertset):
    """Generate function creates files for each dictionary item from the master
    model"""
    #iterate through the dictionary, returning key and value
    for key, value in d.iteritems():
        print "Generating "+ key
        with open(key + '.scad', 'wb') as f:
            with open(model_fn, 'rb') as rd:
                for line in rd: #iterate through the master model
                    didit = False
                    for item in header: #iterate through column names
                        replaceitem = '#'+item #search term
                        if replaceitem in line: #if search term appears in line
                            #replace the value
                            f.write(line.replace('#'+item,value[item]))
                            didit = True
                    #if we didn't replace on the line, just add it as-is
                    if didit == False:
                        f.write(line)
    if convertset == 1: #call the convert function if set
        convert(d)


def convert(d):
    """Convert function calls an external program to compile each of the models
    generated from the dictionary."""
    for key, value in d.iteritems(): #iterating through dict for key, value
        print "Converting " + key
        #this makes command
        command = "openscad.exe -o " + key+'.stl ' + key+'.scad'
        print command
        #this runs command
        print subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,\
                                 stderr=subprocess.STDOUT)

##    #for freecad
##    in_fn, out_fn = sys.argv[2], sys.argv[3]
##    Part.open(in_fn)
##    o = [ FreeCAD.getDocument("Unnamed").findObjects()[0] ]
##    Mesh.export(o, out_fn)


worklist()
