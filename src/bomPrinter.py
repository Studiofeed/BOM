#!/usr/bin/python
'''
Created on 2012-04-17

@author: timvb
'''
import os
import bomOrganizer as bo
import schematicParser as sp

class BOMPrintError(Exception):
    pass

class BaseBOMPrinter(object):
    '''
    Base Class to handle printing of BOM Organized Lists.  
    
    Arguments are:
    filename - The file to print.  
    '''
    def __init__(self, filename, data, attributes=['refdes', 'quantity'], **kwargs):
        
        self.filename = filename
        self.data = data #BOMOrganizer
        if not isinstance(self.data, bo.BOMOrganizer):
            raise TypeError("data argument must be of type bomOrganizer.BOMOrganizer")
        
        self.attributes = attributes
        self.majorDelimiter = kwargs.get('majorDelimiter', ',') #Default comma delimited data 
        self.minorDelimiter = kwargs.get('minorDelimiter', ' ')
        
        if self.majorDelimiter == self.minorDelimiter:
            raise ValueError("Major and Minor Delimiters cannot be Equal")
            
        self.doPrintHeader = kwargs.get('header', True)
        
    def openBOMFile(self):
        
        try:
            self.fp = open(self.filename, 'w')
        except:
            self.fp = None
            return False
        
        else:
            return True

    def formatRefdes(self, refdes):
        '''
        Helper function to format the refdes list into a more printable format
        '''
        
        line = ""
        for item in refdes:
            line +=item
            line += self.minorDelimiter
            
        
        line = line[0:-len(self.minorDelimiter)]
        return line
    
    def printBOM(self):
        if not self.openBOMFile():
            raise BOMPrintError("File could not be opened for printing: %s.\nAborting Print"%(self.filename))
        
        if self.doPrintHeader:
            self.printHeader()
            
        for bomComponent in self.data:
            self.printBOMComponent(bomComponent)
    
    def printAttributes(self):
        line = ""
        for attribute in self.attributes:
            line += attribute
            line += self.majorDelimiter
        line = line[0:-len(self.majorDelimiter)]
        line += os.linesep
        self.fp.write(line)
                
    def printHeader(self):
        import datetime
        header = '''--------------------------------------------------
Bill Of Materials for project: %s
Automatically Generated On %s
--------------------------------------------------
'''%(self.filename, datetime.datetime.now().ctime())
        self.fp.write(header)
        self.printAttributes()
        
    def printBOMComponent(self, component):
        
        line = ""
        for attribute in self.attributes:
            if attribute == "refdes":
                line += self.formatRefdes(component.getAttribute(attribute))
                
            else:
                line += str(component.getAttribute(attribute))
            line += self.majorDelimiter
            
        line = line[:-len(self.majorDelimiter)]
        
        line += os.linesep
        self.fp.write(line)