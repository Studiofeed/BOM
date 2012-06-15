'''
bomReporter takes a delimted bom file from i.e. gnetlist -g bom2 and analyzes and reports on the components

Maybe expand in future to parse gschem .sch files
'''

import os, sys
import csv
import logging
from optparse import OptionParser
import schematicParser
import bomParser

__version__ = "0.0.1"
__author__ = "Tim van Boxtel"
__corporation__ = "SF Labs"

_requiredFields = ["refdes", "value", "vendor", "vendor-number"]
_allowedVendors = ["Digikey"]

def createOptionsParser():
    usage = "bomReporter [options] arg"
    parser = OptionParser(usage=usage, version=__version__)
    parser.add_option("-o","--output",dest="outfile",help="Defines the filename of the reported BOM")
    parser.add_option("-t", "--type", action="store", dest="type", default="csv", help="Define the type of BOM report that is desired.  Allowed values: pdf, csv, ods")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="Executes the program verbosely")
    parser.add_option("-V", "--vendor", dest="vendor", help="Output additional BOM specific to one vendor")
    parser.add_option('-s', '--schematic', dest='schematic_flag', action='store_true', help='Flag to read in gschem schematic file instead of processed bom file')
    return parser

def checkComponentsHaveRequiredFields(components, verbose=False):
    
    new_components = []
    for component in components:
        missingRequiredAttributes = []
        for attribute in _requiredFields:
            
            if not component.hasAttribute(attribute):
                missingRequiredAttributes.append(attribute)
                
        
        if len(missingRequiredAttributes) is not 0:
            if verbose:
                print "Component %s missing the following attributes and will be ignored: %s"%(str(component), str(missingRequiredAttributes))    
            
        else:
            new_components.append(component)
            
                
    return new_components


    
if __name__ == '__main__':

    parser = createOptionsParser()
    (options, args) = parser.parse_args()
    
    if len(args) != 1:
        parser.error("Invalid number of arguments.  Check help")
    
    argfile = args[0]
    if not os.path.isfile(argfile):
        print "File not found: %s.  Exiting"%(argfile)
        sys.exit(1)
    if options.verbose:
        print "File to analyze: %s"%(argfile)
    

    if not options.outfile:
        name, ext =os.path.splitext(argfile)
        
        if options.type == "pdf":
        #Output name is not defined
        #Duplicate name to .pdf
            outFile = name + ".pdf"
            
        elif options.type == "csv":
            outFile = name + ".csv"
    else:
        outFile = options.outfile
    
    verbose = options.verbose
    
    
    if options.schematic_flag:
        #Read schematic file
        print "Reading schematic file: %s"%(argfile) 
        sParser = schematicParser.SchematicParser(argfile)   
        try:
            components = sParser.parse()
        except schematicParser.SchematicParserError, msg:
            print "Error while parsing schematic file: %s"%(msg)
            print "Exiting"
            sys.exit(1)
    
    else:
        #Read Partslist file
        fParser = bomParser.PartsListParser(argfile)
        
        try:
            components = fParser.parse()
        except bomParser.BOMParserError, msg:
            print "Error while parsing partslist file: %s"%(msg)
            print "Exiting"
            sys.exit(1)

    components = checkComponentsHaveRequiredFields(components, verbose)
    
    print "A total of %i valid components to be included in BOM"%(len(components))
    
    